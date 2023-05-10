import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import (
    reverse,
    reverse_lazy
)
from django.utils.decorators import method_decorator
from django.db import transaction
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    FormView,
    TemplateView
)
from django.views.generic.detail import SingleObjectMixin

from cart_app import cart
from cart_app.cart import Cart
from donut_app.forms import OrderCreate
from donut_app.models import Donut, Order, OrderItem


class CreateOrderView(FormView):
    template_name = 'donut/cart.html'
    form_class = OrderCreate
    success_url = reverse_lazy('donut:donut_list')

    @transaction.atomic
    def form_valid(self, form):
        cart_obj = cart.Cart(self.request)
        customer_name = form.cleaned_data['customer_name']
        customer_email = form.cleaned_data['customer_email']
        customer_address = form.cleaned_data['customer_address']
        items = cart_obj.get_items()
        total_price = (cart_obj.get_total_price(self))

        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_address=customer_address,
            total_price=total_price,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                donut=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_token = self.request.POST.get('stripeToken')

        line_items = []
        for item in items:
            item_dict = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            }
            line_items.append(item_dict)

        checkout_session = stripe.checkout.Session.create(
            success_url=reverse('order:success'),
            cancel_url=reverse('order:cancel'),
            mode='payment',
            line_items=line_items,
        )

        return HttpResponseRedirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = 'success.html'


    def get_context_data(self, **kwargs):
        cart = self.cart(self.request)
        form = OrderCreate()
        context = {
            'cart': cart,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'total_price': cart.get_total_price() * 100,
            'form': form,
        }
        return context


class AddToCartView(SingleObjectMixin, View):
    model = Donut

    def post(self, request, *args, **kwargs):
        donut = self.get_object()
        cart = Cart(request)
        cart_item = cart.get(donut.id)
        if donut.count > 0:
            if cart_item is None:
                cart.add(donut)
                donut.count -= 1
                donut.save()
            else:
                donut.count -= 1
                donut.save()
                cart_item['quantity'] += 1
                cart.save()
        else:
            messages.error(
                request, 'This donut is ended, please, take some other!'
            )
        return redirect(request.META.get('HTTP_REFERER', 'donut:donut_list'))


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCartView(SingleObjectMixin, View):
    model = Donut

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            donut = self.get_object()
            cart = Cart(request)
            cart_item = cart.get(donut.id)
            if cart_item is not None:
                if cart_item['quantity'] > 1:
                    cart_item['quantity'] -= 1
                    cart.save()
                else:
                    cart.remove(donut)
                donut.count += 1
                donut.save()
            else:
                messages.error(request, 'Add donut to your cart!')
            return redirect(reverse('cart:cart'))

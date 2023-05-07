from donut_app.models import (
    Donut,
    Order,
)
from donut_app.forms import (
    OrderCreate,
    OrderItem
)
from cart_app import cart
from django.conf import settings
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    FormView
)
from django.shortcuts import (
    render,
    redirect
)
from django.views.generic import(
    ListView,
    DetailView,
    TemplateView,
    CreateView,

)
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from donut_app.models import (
    Donut,
    Order,
    OrderItem
)
from donut_app.forms import OrderCreate
from django.contrib import messages
from cart_app.cart import Cart
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from cart_app import cart
import stripe

class CreateOrderView(FormView):
    template_name = 'donut/cart.html'
    form_class = OrderCreate
    model = Order
    success_url = 'donut:donut_list'
    cart = cart.Cart

    def form_valid(self, form):
        cart = self.cart(self.request)
        customer_name = form.cleaned_data['customer_name']
        customer_email = form.cleaned_data['customer_email']
        customer_address = form.cleaned_data['customer_address']
        items = cart.get_items()
        total_price = cart.get_total_price(self)

        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_address=customer_address,
            total_price=total_price
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                donut=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_token = self.request.POST.get('stripeToken')

            try:
                charge = stripe.Charge.create(
                    amount=int(order.total_price * 100),
                    currency='usd',
                    description='Payment Gateway',
                    source=stripe_token,
                )
                order.paid = True
                order.save()
                cart.clear()
                print(order)
                return super().form_valid(form)

            except stripe.error.CardError as e:
                error_msg = e.json_body['error']['message']
                return render(self.request, 'donut/cart.html', {'error': error_msg})

    def get_context_data(self, **kwargs):
        cart = self.cart(self.request)
        form = OrderCreate()
        context = {
            'cart': cart,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'total_price': cart.get_total_price()*100,
            'form': form
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
            messages.error(request, 'This donut is ended, please, take some other!')
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

import stripe
import json
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from cart_app import cart
from cart_app.cart import Cart
from donut_app.forms import OrderCreate
from donut_app.models import Donut, Order, OrderItem


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
            total_price=total_price,
        )

        for item in items:
            order_items = OrderItem.objects.create(
                order=order,
                donut=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_token = self.request.POST.get('stripeToken')

        def create_checkout_session(order_items):
            quantity = request.form.get('quantity', 1)
            domain_url = os.getenv('DOMAIN')

            try:
                checkout_session = stripe.checkout.Session.create(
                    success_url=domain_url + '/success.html?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + '/canceled.html',
                    mode='payment',
                    line_items=[],
                    for items in order_items:
                        item_dict = {
                            price_data : {items.donut.price},
                            quantity : item.quantity
                        }
                        line_items.append(item_dict)
                )
                return redirect(checkout_session.url, code=303)
            except Exception as e:
                return jsonify(error=str(e)), 403

        @app.route('/webhook', methods=['POST'])
        def webhook_received():
            data = request_data['data']
            event_type = request_data['type']
            data_object = data['object']

            print('event ' + event_type)

            if event_type == 'checkout.session.completed':
                print('🔔 Payment succeeded!')

            return jsonify({'status': 'success'})




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

from decimal import Decimal
from donut_app.models import (
    Donut,
    Order,
)
from donut_app.forms import OrderCreate
from django.conf import settings
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    FormView
)
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, donut, quantity=1):
        donut_id = str(donut.id)
        if donut_id not in self.cart:
            self.cart[donut_id] = {'quantity': 0, 'price': str(donut.price)}
        self.cart[donut_id]['quantity'] += quantity
        self.save()

    def get(self, donut_id):
        if str(donut_id) in self.cart:
            return self.cart[str(donut_id)]
        return None

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )

    def save(self):
        self.session.modified = True

    def remove(self, donut):
        donut_id = str(donut.id)
        if donut_id in self.cart:
            del self.cart[donut_id]
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_context_data(self):
        context = {}
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        cart = Cart(self.request)
        context['total_price'] = cart.get_total_price()
        return context

    def __iter__(self):
        donut_ids = self.cart.keys()
        donuts = Donut.objects.filter(id__in=donut_ids)
        for donut in donuts:
            self.cart[str(donut.id)]['donut'] = donut

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


# def charge(request):
#     if request.method == 'POST':
#         stripe_token = request.POST['stripeToken']
#         amount = Cart(request).get_total_price()
#         stripe.api_version = "2022-08-01"
#         try:
#             charge = stripe.Charge.create(
#                 amount=int(amount * 100),
#                 currency='usd',
#                 description='Payment Gateway',
#                 source=stripe_token
#             )
#         except stripe.error.CardError as e:
#             pass
#     Cart.clear()
#     Cart.save()
#     return render(request, 'home.html')
#
# class CreateOrderView(CreateView):
#     model = Order
#     form_class = OrderCreate
#     # redirect_field_name = 'donut_app/donut_list'
#     template_name = 'donut/cart.html'
#
#     def form_valid(self, form):
#         cart = Cart(self.request)
#         cart.clear()
#         order = form.save()
#         return super().form_valid(form)
#

class CreateOrderView(FormView):
    template_name = 'donut/cart.html'
    form_class = OrderCreate
    model = Order
    success_url = 'donut:donut_list'

    def form_valid(self, form):
        stripe_token = self.request.POST.get('stripeToken')
        total_price = self.request.POST.get('total_price')

        charge = stripe.Charge.create(
            amount=int(total_price * 100),
            currency='usd',
            description='Payment Gateway',
            source=stripe_token,
        )

        order = form.save()
        # order.payment_id = charge.id
        order.save()
        cart = Cart(self.request)
        cart.clear()
        cart.save()

        return super().form_valid(form)

    def get_context_data(self):
        cart = Cart(self.request)
        form = OrderCreate
        context = {
            'cart': cart,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'total_price': cart.get_total_price()*100,
            'form': form
        }
        return context



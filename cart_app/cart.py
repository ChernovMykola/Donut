from decimal import Decimal
from donut_app.models import Donut, Order
from django.conf import settings
from django.shortcuts import render
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


def charge(request):
    if request.method == 'POST':
        stripe_token = request.POST['stripeToken']
        amount = Cart(request).get_total_price()
        stripe.api_version = "2022-08-01"
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency='usd',
                description='Payment Gateway',
                source=stripe_token
            )
        except stripe.error.CardError as e:
            pass
    Cart.clear()
    Cart.save()
    return render(request, 'home.html')

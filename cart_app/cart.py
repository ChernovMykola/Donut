from decimal import Decimal

import stripe
from django.conf import settings

from donut_app.models import Donut

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
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
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

    def get_items(self):
        donut_ids = self.cart.keys()
        donuts = Donut.objects.filter(id__in=donut_ids)
        items = []
        for donut in donuts:
            item = {
                'name': donut.name,
                'price': float(self.cart[str(donut.id)]['price']),
                'quantity': self.cart[str(donut.id)]['quantity'],
            }
            items.append(item)
        return items

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

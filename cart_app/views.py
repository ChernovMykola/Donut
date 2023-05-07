from donut_app.models import (
    Donut,
    Order,
)
from donut_app.forms import (
    OrderCreate,
    OrderItem
)
from django.conf import settings
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    FormView
)
import stripe
# Create your views here.
class CreateOrderView(FormView):
    template_name = 'donut/cart.html'
    form_class = OrderCreate
    model = Order
    success_url = 'donut:donut_list'

    def form_valid(self, form):
        cart = Cart(self.request)
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
        cart = Cart(self.request)
        form = OrderCreate()
        context = {
            'cart': cart,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'total_price': cart.get_total_price()*100,
            'form': form
        }
        return context

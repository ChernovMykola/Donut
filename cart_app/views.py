import os
import smtplib
from email.mime.text import MIMEText
import stripe
from django.conf import settings
from django.contrib import messages
from django.http import (
    HttpResponseRedirect
)
from django.shortcuts import (
    redirect,
)
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
    TemplateView,
)
from django.views.generic.detail import SingleObjectMixin
from cart_app import cart
from cart_app.cart import Cart
from donut_app.forms import OrderCreate
from donut_app.models import (
    Donut,
    Order,
    OrderItem
)

class CreateOrderView(FormView):
    template_name = 'donut/cart.html'
    form_class = OrderCreate
    success_url = reverse_lazy('donut:donut_list')

    def get_context_data(self, **kwargs):
        cart_obj = cart.Cart(self.request)
        form = OrderCreate()
        context = {
            'cart': cart_obj,
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'total_price': cart_obj.get_total_price() * 100,
            'form': form,
        }
        return context

    @transaction.atomic
    def form_valid(self, form):
        cart_obj = cart.Cart(self.request)
        customer_name = form.cleaned_data['customer_name']
        customer_email = form.cleaned_data['customer_email']
        customer_address = form.cleaned_data['customer_address']
        items = cart_obj.get_items()
        total_price = cart_obj.get_total_price()

        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_address=customer_address,
            total_price=total_price,
        )
        # order.items.set(Donut.objects.filter(id__in=[item['id'] for item in items]))

        for item in items:
            donut = Donut.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                donut=donut,
                quantity=item['quantity'],
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        stripe_token = self.request.POST.get('stripeToken')

        line_items = []
        for item in items:
            item_dict = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name']
                    },
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            }
            line_items.append(item_dict)

        checkout_session = stripe.checkout.Session.create(
            success_url='http://daniilchernov.pythonanywhere.com/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=f'http://daniilchernov.pythonanywhere.com/{reverse("order:cancel")}',
            mode='payment',
            line_items=line_items,
        )
        order.session_id = checkout_session.id
        order.save()
        cart.Cart.clear(self.request)
        cart.Cart.save(self.request)
        return HttpResponseRedirect(checkout_session.url)


class SuccessView(View):

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        order = Order.objects.get(session_id=session_id)
        order.paid = True
        order.save()

        sender = 'DonutEcc@gmail.com'
        password = os.getenv("EMAIL_PASSWORD")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(sender,password)
            msg_text = f"Thank you for your order, {order.customer_name}!\n\n"
            msg_text += "Here is a summary of your order:\n\n"
            for item in order.orderitem_set.all():
                msg_text += f"- {item.donut.name} x {item.quantity}: ${item.donut.price * item.quantity:.2f}\n"
            msg_text += f"\nTotal price: ${order.total_price:.2f}\n"
            msg_text += "\nSee you!\n"
            msg = MIMEText(msg_text)
            msg["Subject"] = "ORDER!"
            server.sendmail(sender, order.customer_email, msg.as_string())
        except Exception as _ex:
            return f"{_ex}\nProblems with your order!"

        return redirect('order:thank_you')


class ThankView(TemplateView):
    template_name = 'donut/success.html'



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

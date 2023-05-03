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
from donut_app.models import Donut
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from .models import (
    Donut,
    Order,
    OrderItem
)
from .forms import OrderCreate
from django.contrib import messages
from cart_app.cart import Cart
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


class DonutListView(ListView):
    model = Donut
    paginate_by = 6
    template_name = 'donut/home.html'
    context_object_name = 'donut'
    def get_queryset(self):
        donut = Donut.objects.all().order_by('id')
        return donut





class DonutDetailView(DetailView):
    model = Donut
    template_name = 'donut/donut_detail.html'
    context_object_name = 'donut'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class AddToCartView(SingleObjectMixin, View):
    model = Donut

    def post(self, request, *args, **kwargs):
        donut = self.get_object()
        cart = Cart(request)
        cart_item = cart.get(donut.id)
        if cart_item is None:
            cart.add(donut)
            donut.count -= 1
            donut.save()
        else:
            if donut.count != 0:
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
            return redirect(reverse('donut:cart'))


def view_cart(request):
    cart = Cart(request)
    print("Cart contents:", cart.cart)
    cart.clear()
    print("Cart contents after clearing:", cart.cart)
    context = {
        'cart':cart,
        'key':settings.STRIPE_PUBLISHABLE_KEY,
        'total_price': cart.get_total_price()*100,
    }
    return render(request, 'donut/cart.html', context)


class CreateOrderView(CreateView):
    model = Order
    form_class = OrderCreate



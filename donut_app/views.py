from django.shortcuts import (
    render,
    redirect
)
from django.views.generic import(
    ListView,
    DetailView,
    TemplateView,
)
from donut_app.models import Donut
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from .models import Donut
from django.contrib import messages
from cart_app.cart import Cart
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


class DonutListView(ListView):
    model = Donut
    paginate_by = 5
    template_name = 'donut/home.html'
    context_object_name = 'donut'

class DonutDetailView(DetailView):
    model = Donut
    template_name = 'donut/donut_detail.html'
    context_object_name = 'donut'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddToCartView(SingleObjectMixin, View):
    model = Donut
    donut_test = 10

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
        return redirect(reverse('donut:donut_list'))

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
    context = {
        'cart': cart
    }
    return render(request, 'donut/cart.html', context)
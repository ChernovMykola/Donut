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

    def post(self, request, *args, **kwargs):
        donut = self.get_object()
        cart = Cart(request)
        cart_item = cart.get(donut.id)
        if cart_item is None:
            cart.add(donut)
        else:
            if donut.count > 0 :
                donut.count -= 1
                donut.save()
                cart_item['quantity'] += 1
                cart.save()
            else:
                messages.error(request, 'This donut is ended, please, take some other!')
        return redirect(reverse('donut:donut_list'))

def view_cart(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'donut/cart.html', context)
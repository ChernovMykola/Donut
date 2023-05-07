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
from donut_app.models import (
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
from cart_app import cart

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












from django.shortcuts import render
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from donut_app.models import Donut

class DonutListView(ListView):
    model = Donut
    template_name = 'donut/home.html'


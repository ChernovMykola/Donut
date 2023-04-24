from django.shortcuts import render
from django.views.generic import(
    ListView,
    DetailView,
    TemplateView,
)
from donut_app.models import Donut

class DonutListView(ListView):
    model = Donut
    template_name = 'donut/home.html'
    context_object_name = 'donut'

class DonutDetailView(DetailView):
    model = Donut
    template_name = 'donut/donut_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
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

class DonutDetailView(DetailView):
    model = Donut

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
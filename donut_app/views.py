from django.views.generic import DetailView, ListView

from .models import Donut


class DonutListView(ListView):
    model = Donut
    paginate_by = 6
    template_name = 'donut/home.html'
    context_object_name = 'donut'

    def get_queryset(self):
        donut = Donut.objects.all().order_by('id')
        label = self.request.GET.get('label')
        if label:
            donut = Donut.objects.filter(labels__contains=label).order_by('id')
        return donut

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        label = self.request.GET.get('label')
        context['selected_label'] = label
        return context



class DonutDetailView(DetailView):
    model = Donut
    template_name = 'donut/donut_detail.html'
    context_object_name = 'donut'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

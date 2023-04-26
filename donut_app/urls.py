from django.urls import path
from . import views

app_name = 'donut'

urlpatterns = [
    path('',
views.DonutListView.as_view(), name='donut_list'),
    path('<int:pk>/',
views.DonutDetailView.as_view(), name='donut_detail'),
]
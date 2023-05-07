from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'donut'

urlpatterns = [
    path('',
views.DonutListView.as_view(), name='donut_list'),
    path('<int:pk>/',
views.DonutDetailView.as_view(), name='donut_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
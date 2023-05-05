from django.urls import path
from . import views
from cart_app import cart
from django.conf import settings
from django.conf.urls.static import static

app_name = 'donut'

urlpatterns = [
    path('',
views.DonutListView.as_view(), name='donut_list'),
    path('<int:pk>/',
views.DonutDetailView.as_view(), name='donut_detail'),
    path('cart/',
cart.CreateOrderView.as_view(), name='cart'),
    path('add_to_cart/<int:pk>/',
views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',
views.RemoveFromCartView.as_view(), name='remove_from_cart'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
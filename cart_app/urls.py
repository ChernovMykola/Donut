
from django.urls import path
from cart_app import views

app_name = 'order'

urlpatterns = [
    path('create_order/',
views.CreateOrderView.as_view(), name='create_order'),
    path('cart/',
views.CreateOrderView.as_view(), name='cart'),

]
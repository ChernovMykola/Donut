
from django.urls import path
from cart_app import cart

app_name = 'order'

urlpatterns = [
    path('create_order/',
cart.CreateOrderView.as_view(), name='create_order'),

]
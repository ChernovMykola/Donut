from django.urls import path
from . import views
from cart_app import cart

app_name = 'donut'

urlpatterns = [
    path('',
views.DonutListView.as_view(), name='donut_list'),
    path('<int:pk>/',
views.DonutDetailView.as_view(), name='donut_detail'),
    path('cart/',
views.view_cart, name='cart'),
    path('add_to_cart/<int:pk>/',
views.AddToCartView.as_view(), name='add_to_cart'),

]
from django.urls import path

from cart_app import views

app_name = 'order'

urlpatterns = [
    # path(
    #     'create_order/',
    #     views.CreateOrderView.as_view(),
    #     name='create_order'
    # ),
    path(
        'cart/',
        views.CreateOrderView.as_view(),
        name='cart'),
    path(
        'add_to_cart/<int:pk>/',
        views.AddToCartView.as_view(),
        name='add_to_cart',
    ),
    path(
        'remove_from_cart/<int:pk>/',
        views.RemoveFromCartView.as_view(),
        name='remove_from_cart',
    ),
    path(
        'success/',
        views.SuccessView.as_view(),
        name='success',
    ),
    path(
        'cancel/',
        views.CreateOrderView.as_view(),
        name='cancel',
    )
]

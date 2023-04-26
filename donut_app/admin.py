from django.contrib import admin
from donut_app.models import (
    Donut,
    Order,
    OrderItem
)

admin.site.register(Donut)
admin.site.register(Order)
admin.site.register(OrderItem)


from django import forms
from donut_app.models import (
    Donut,
    Order,
    OrderItem
)


class OrderCreate(forms.ModelForm):
    class Meta():
        model = Order

        fields = ('customer_name', 'customer_email', 'customer_address', 'items')

        widgets = {

        }

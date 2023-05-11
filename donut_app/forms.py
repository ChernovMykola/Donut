from django import forms
from donut_app.models import Order
from cart_app import cart


class OrderCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_email',
            'customer_address',
        ]

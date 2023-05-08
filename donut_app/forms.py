from django import forms

from donut_app.models import Order


class OrderCreate(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_email',
            'customer_address',
            'items',
        ]

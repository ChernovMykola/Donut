from django import forms
from donut_app.models import (
    Donut,
    Order,
    OrderItem
)


# class OrderCreate(forms.ModelForm):
#     items = forms.ModelMultipleChoiceField(
#         queryset=Donut.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     class Meta():
#         model = Order
#         fields = ('customer_name', 'customer_email', 'customer_address')
#
#         widgets = {
#
#         }

class OrderCreate(forms.ModelForm):
    # items = forms.ModelMultipleChoiceField(
    #     queryset=Donut.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_address', 'items']

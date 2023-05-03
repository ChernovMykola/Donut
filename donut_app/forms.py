from django import forms
from donut_app.models import (
    Donut,
    Order,
    OrderItem
)

class OrderCreate(forms.ModelForm):
    class Meta():
        model = Order
        fields = ('customer_name', 'customer_email', 'customer_address', 'items', 'total_price')
        widgets = {
            # 'customer_name': forms.TextInput(attrs={'class': 'textinputclass'}),
            # 'customer_adress': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

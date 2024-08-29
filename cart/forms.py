from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        return quantity
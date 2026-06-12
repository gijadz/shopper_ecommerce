from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm): #form per creare/modificare un prodotto
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category']

    #esempio di validazione custom: mi assicuro che il valore è positivo
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Il prezzo deve essere maggiore di zero!")
        return price

class OrderCreateForm(forms.ModelForm): #form per creare un ordine
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
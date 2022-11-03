from django import forms
from .models import Products, Location

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = (
            'title',
            'content',
            'original_image',
            'price',
        )
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            'trade_locationx',
            'trade_locationy',
        )
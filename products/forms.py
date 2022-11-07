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

        labels = {
            "title": "제목",
            "content":"내용",
            "original_image":"이미지",
            "price" : "가격(원)",
        }
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            'trade_locationx',
            'trade_locationy',
        )
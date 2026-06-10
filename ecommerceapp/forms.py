from .models import *
from django import forms

class productForm(forms.ModelForm):
    class Meta:
        model= AddProduct
        fields= '__all__'
 

class categoryForm(forms.ModelForm):
    class Meta:
        model= category
        fields= '__all__'
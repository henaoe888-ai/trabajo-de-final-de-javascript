from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'required': True}),
            'stock': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'required': True}),
        }

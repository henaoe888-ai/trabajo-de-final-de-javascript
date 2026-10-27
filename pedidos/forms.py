from django import forms
from .models import Pedido
from productos.models import Producto

class RealizarPedidoForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(stock__gt=0),
        empty_label="-- Selecciona una Joya --",
        widget=forms.Select(attrs={'class': 'form-input', 'required': True})
    )
    direccion = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dirección completa de entrega', 'required': True})
    )

    class Meta:
        model = Pedido
        fields = ['producto', 'direccion']

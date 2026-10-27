from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    ROL_CHOICES = (
        ('CLIENTE', 'Cliente'),
        ('EMPLEADO', 'Empleado'),
    )
    rol = forms.ChoiceField(choices=ROL_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="Rol a registrar")
    foto_perfil = forms.ImageField(required=False, label="Foto de Perfil")
    direccion = forms.CharField(max_length=255, required=False, label="Dirección de Envío (solo para clientes)", widget=forms.TextInput(attrs={'placeholder': 'Ej. Calle 10 # 5-20'}))

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'rol', 'foto_perfil', 'direccion')

class PerfilEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'area_trabajo', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'required': True}),
            'area_trabajo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Ventas, Taller de Oro, Mostrador', 'required': True}),
        }

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'direccion', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Carrera 45 # 12-34', 'required': True}),
        }

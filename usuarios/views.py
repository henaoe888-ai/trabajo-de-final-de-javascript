from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, PerfilEmpleadoForm, PerfilClienteForm

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('redirect_por_rol')
        
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('redirect_por_rol')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('redirect_por_rol')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('redirect_por_rol')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def redirect_por_rol(request):
    user = request.user
    if user.rol == 'ADMIN' or user.is_superuser:
        return redirect('panel_admin')
    elif user.rol == 'EMPLEADO':
        return redirect('panel_empleado')
    else:
        return redirect('panel_cliente')

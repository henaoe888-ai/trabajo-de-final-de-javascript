from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm

@login_required
def crear_producto(request):
    if request.user.rol != 'ADMIN' and not request.user.is_superuser:
        return redirect('redirect_por_rol')
        
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = ProductoForm()
    return render(request, 'productos/form_producto.html', {'form': form, 'titulo': 'Agregar Nueva Joya'})

@login_required
def editar_producto(request, producto_id):
    if request.user.rol != 'ADMIN' and not request.user.is_superuser:
        return redirect('redirect_por_rol')
        
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form_producto.html', {'form': form, 'titulo': 'Editar Joya', 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    if request.user.rol != 'ADMIN' and not request.user.is_superuser:
        return redirect('redirect_por_rol')
        
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('panel_admin')
    return render(request, 'productos/confirmar_eliminar_producto.html', {'producto': producto})

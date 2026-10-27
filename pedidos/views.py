from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Pedido
from .forms import RealizarPedidoForm
from productos.models import Producto
from usuarios.forms import PerfilEmpleadoForm, PerfilClienteForm

def limpiar_pedidos_expirados():
    ahora = timezone.now()
    Pedido.objects.filter(estado='PENDIENTE', limite_confirmacion__lt=ahora).delete()

# --- PANEL ADMIN ---
@login_required
def panel_admin(request):
    if request.user.rol != 'ADMIN' and not request.user.is_superuser:
        return redirect('redirect_por_rol')
    
    limpiar_pedidos_expirados()
    pedidos = Pedido.objects.all().order_by('-fecha_registro')
    productos = Producto.objects.all().order_by('-id')

    return render(request, 'pedidos/panel_admin.html', {
        'usuario': request.user,
        'pedidos': pedidos,
        'productos': productos
    })

@login_required
def eliminar_pedido_admin(request, pedido_id):
    if request.user.rol != 'ADMIN' and not request.user.is_superuser:
        return redirect('redirect_por_rol')

    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('panel_admin')
        
    return render(request, 'pedidos/confirmar_eliminar_pedido.html', {'pedido': pedido})


# --- PANEL EMPLEADO ---
@login_required
def panel_empleado(request):
    if request.user.rol != 'EMPLEADO':
        return redirect('redirect_por_rol')

    limpiar_pedidos_expirados()

    if request.method == 'POST':
        if 'actualizar_perfil' in request.POST:
            form_perfil = PerfilEmpleadoForm(request.POST, request.FILES, instance=request.user)
            if form_perfil.is_valid():
                form_perfil.save()
                return redirect('panel_empleado')
        elif 'cambiar_estado_pedido' in request.POST:
            pedido_id = request.POST.get('pedido_id')
            nuevo_estado = request.POST.get('estado')
            pedido = get_object_or_404(Pedido, id=pedido_id)
            if nuevo_estado in ['PENDIENTE', 'APROBADO', 'ENTREGADO']:
                pedido.estado = nuevo_estado
                pedido.save()
            return redirect('panel_empleado')

    form_perfil = PerfilEmpleadoForm(instance=request.user)
    pedidos = Pedido.objects.all().order_by('-fecha_registro')
    productos = Producto.objects.all()

    return render(request, 'pedidos/panel_empleado.html', {
        'usuario': request.user,
        'form_perfil': form_perfil,
        'pedidos': pedidos,
        'productos': productos
    })


# --- PANEL CLIENTE ---
@login_required
def panel_cliente(request):
    if request.user.rol != 'CLIENTE':
        return redirect('redirect_por_rol')

    limpiar_pedidos_expirados()

    if request.method == 'POST':
        if 'actualizar_perfil' in request.POST:
            form_perfil = PerfilClienteForm(request.POST, request.FILES, instance=request.user)
            if form_perfil.is_valid():
                form_perfil.save()
                return redirect('panel_cliente')
        elif 'realizar_pedido' in request.POST:
            form_pedido = RealizarPedidoForm(request.POST)
            if form_pedido.is_valid():
                pedido = form_pedido.save(commit=False)
                pedido.cliente = request.user
                pedido.nombre_cliente = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
                pedido.nombre_producto = pedido.producto.nombre
                pedido.valor_total = pedido.producto.precio
                pedido.save()
                return redirect('panel_cliente')

    form_perfil = PerfilClienteForm(instance=request.user)
    form_pedido = RealizarPedidoForm(initial={'direccion': request.user.direccion or ''})
    mis_pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_registro')

    return render(request, 'pedidos/panel_cliente.html', {
        'usuario': request.user,
        'form_perfil': form_perfil,
        'form_pedido': form_pedido,
        'mis_pedidos': mis_pedidos
    })

@login_required
def cancelar_pedido_cliente(request, pedido_id):
    if request.user.rol != 'CLIENTE':
        return redirect('redirect_por_rol')

    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    if request.method == 'POST':
        pedido.estado = 'CANCELADO'
        pedido.save()
        return redirect('panel_cliente')
        
    return render(request, 'pedidos/confirmar_cancelar_pedido.html', {'pedido': pedido})

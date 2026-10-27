from django.urls import path
from . import views

urlpatterns = [
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-admin/eliminar-pedido/<int:pedido_id>/', views.eliminar_pedido_admin, name='eliminar_pedido_admin'),
    path('panel-empleado/', views.panel_empleado, name='panel_empleado'),
    path('panel-cliente/', views.panel_cliente, name='panel_cliente'),
    path('panel-cliente/cancelar-pedido/<int:pedido_id>/', views.cancelar_pedido_cliente, name='cancelar_pedido_cliente'),
]

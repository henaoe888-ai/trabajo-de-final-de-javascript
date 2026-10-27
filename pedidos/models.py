from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from productos.models import Producto

class Pedido(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pedidos')
    nombre_cliente = models.CharField(max_length=150)
    nombre_producto = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    limite_confirmacion = models.DateTimeField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')

    def save(self, *args, **kwargs):
        if not self.id and not self.limite_confirmacion:
            self.limite_confirmacion = timezone.now() + timedelta(minutes=30)
        if self.cliente and not self.nombre_cliente:
            self.nombre_cliente = f"{self.cliente.first_name} {self.cliente.last_name}".strip() or self.cliente.username
        if self.producto and not self.nombre_producto:
            self.nombre_producto = self.producto.nombre
        if self.producto and not self.valor_total:
            self.valor_total = self.producto.precio
        super().save(*args, **kwargs)

    def tiempo_restante_minutos(self):
        ahora = timezone.now()
        if ahora >= self.limite_confirmacion:
            return 0
        diferencia = self.limite_confirmacion - ahora
        return int(diferencia.total_seconds() // 60)

    def esta_expirado(self):
        return timezone.now() >= self.limite_confirmacion and self.estado == 'PENDIENTE'

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente} ({self.estado})"

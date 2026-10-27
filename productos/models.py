from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio:,.0f}"

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('EMPLEADO', 'Empleado'),
        ('CLIENTE', 'Cliente'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='CLIENTE')
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    area_trabajo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Área de trabajo")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección principal")

    # Solución al conflicto de colisión con auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_permissions_set',
        related_query_name='usuario',
    )

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
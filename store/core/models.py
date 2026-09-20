from django.db import models

from django.contrib.auth.models import User

class Cliente(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cliente'
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    provincia = models.CharField(
        max_length=100
    )

    canton = models.CharField(
        max_length=100
    )

    distrito = models.CharField(
        max_length=100
    )

    direccion = models.TextField()

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.usuario.username
    
class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )

    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )

    disponible = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.nombre
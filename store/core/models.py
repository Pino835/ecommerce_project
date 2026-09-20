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


class Carrito(models.Model):

    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='carrito'
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Carrito de {self.cliente}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class CarritoItem(models.Model):

    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='items'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='carrito_items'
    )

    cantidad = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad


class Pedido(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PAGADO = 'pagado', 'Pagado'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGADO = 'entregado', 'Entregado'
        CANCELADO = 'cancelado', 'Cancelado'

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    direccion_envio = models.TextField()

    creado = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Pedido #{self.pk} - {self.cliente}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class PedidoItem(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='pedido_items'
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad
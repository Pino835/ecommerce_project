from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto, Carrito


class CarritoCheckoutTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='juan', password='claveSegura123')
        categoria = Categoria.objects.create(nombre='Computadoras')
        self.producto = Producto.objects.create(
            categoria=categoria,
            nombre='Laptop',
            descripcion='Laptop de prueba',
            precio=Decimal('500.00'),
            stock=5,
        )
        self.client.login(username='juan', password='claveSegura123')

    def test_agregar_al_carrito_crea_item(self):
        response = self.client.post(reverse('carrito_agregar', args=[self.producto.id]))
        self.assertEqual(response.status_code, 302)

        carrito = Carrito.objects.get(cliente__usuario=self.user)
        self.assertEqual(carrito.items.count(), 1)
        self.assertEqual(carrito.total, Decimal('500.00'))

    def test_checkout_crea_pedido_y_descuenta_stock(self):
        self.client.post(reverse('carrito_agregar', args=[self.producto.id]))

        response = self.client.post(reverse('checkout'), {'direccion_envio': 'Casa 123'})
        self.assertEqual(response.status_code, 302)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 4)

        carrito = Carrito.objects.get(cliente__usuario=self.user)
        self.assertEqual(carrito.items.count(), 0)

    def test_checkout_sin_items_redirige_a_carrito(self):
        response = self.client.post(reverse('checkout'))
        self.assertRedirects(response, reverse('carrito'))

from django.urls import path
from .views import (
    login_view, registro_view, hero_view, menu_view, perfil_view, logout_view,
    carrito_view, carrito_agregar_view, carrito_eliminar_view,
    checkout_view, pedido_detalle_view, pedidos_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('', hero_view, name='hero'),
    path('menu/', menu_view, name='menu'),
    path('perfil/', perfil_view, name='perfil'),
    path('logout/', logout_view, name='logout'),
    path('carrito/', carrito_view, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', carrito_agregar_view, name='carrito_agregar'),
    path('carrito/eliminar/<int:item_id>/', carrito_eliminar_view, name='carrito_eliminar'),
    path('checkout/', checkout_view, name='checkout'),
    path('pedidos/', pedidos_view, name='pedidos'),
    path('pedidos/<int:pedido_id>/', pedido_detalle_view, name='pedido_detalle'),
]
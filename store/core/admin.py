from django.contrib import admin
from .models import Cliente, Categoria, Producto, Carrito, CarritoItem, Pedido, PedidoItem

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(CarritoItem)


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'creado')
    list_filter = ('estado',)
    inlines = [PedidoItemInline]

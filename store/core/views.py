from django.contrib.auth.models import User
from .models import Cliente, Producto, Categoria, Carrito, CarritoItem, Pedido, PedidoItem
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

#LOGIN Y REGISTRO
def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(
                request,
                usuario
            )

            return redirect('menu')

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos'
            )

    return render(
        request,
        'login/login.html'
    )

def registro_view(request):
    if request.method == 'POST':
        username   = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        telefono   = request.POST.get('telefono', '')
        provincia  = request.POST.get('provincia')
        canton     = request.POST.get('canton')
        distrito   = request.POST.get('distrito')
        direccion  = request.POST.get('direccion')

        # Validaciones básicas
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'login/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'login/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return render(request, 'login/registro.html')

        # Crear User y Cliente en una sola transacción atómica
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
                Cliente.objects.create(
                    usuario=user,
                    telefono=telefono,
                    provincia=provincia,
                    canton=canton,
                    distrito=distrito,
                    direccion=direccion,
                )
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('login')

        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear la cuenta. Intente de nuevo.')

    return render(request, 'login/registro.html')

def logout_view(request):
    logout(request)
    return redirect('hero')

#CORE

def hero_view(request):
    return render(request, 'core/hero.html')

def menu_view(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    return render(request, 'core/menu.html', {'categorias': categorias, 'productos': productos})

@login_required(login_url='login')
def perfil_view(request):
    cliente, created = Cliente.objects.get_or_create(
        usuario=request.user,
        defaults={
            'telefono': '',
            'provincia': '',
            'canton': '',
            'distrito': '',
            'direccion': '',
        }
    )
    return render(request, 'core/perfil.html', {'cliente': cliente})

#CARRITO Y PEDIDOS

def _get_carrito(request):
    cliente, _ = Cliente.objects.get_or_create(
        usuario=request.user,
        defaults={
            'telefono': '',
            'provincia': '',
            'canton': '',
            'distrito': '',
            'direccion': '',
        }
    )
    carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
    return carrito

@login_required(login_url='login')
def carrito_view(request):
    carrito = _get_carrito(request)
    return render(request, 'core/carrito.html', {'carrito': carrito})

@login_required(login_url='login')
def carrito_agregar_view(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, disponible=True)
    carrito = _get_carrito(request)

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )
    if not created:
        item.cantidad += 1
        item.save()

    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('menu')

@login_required(login_url='login')
def carrito_eliminar_view(request, item_id):
    carrito = _get_carrito(request)
    item = get_object_or_404(CarritoItem, pk=item_id, carrito=carrito)
    item.delete()
    return redirect('carrito')

@login_required(login_url='login')
def checkout_view(request):
    carrito = _get_carrito(request)
    items = list(carrito.items.select_related('producto'))

    if not items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    if request.method == 'POST':
        direccion = request.POST.get('direccion_envio', carrito.cliente.direccion)

        for item in items:
            if item.cantidad > item.producto.stock:
                messages.error(
                    request,
                    f'No hay suficiente stock de {item.producto.nombre}.'
                )
                return redirect('carrito')

        with transaction.atomic():
            pedido = Pedido.objects.create(
                cliente=carrito.cliente,
                direccion_envio=direccion,
            )
            for item in items:
                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                )
                item.producto.stock -= item.cantidad
                item.producto.save()

            carrito.items.all().delete()

        messages.success(request, '¡Pedido realizado con éxito!')
        return redirect('pedido_detalle', pedido_id=pedido.pk)

    return render(request, 'core/checkout.html', {'carrito': carrito, 'items': items})

@login_required(login_url='login')
def pedido_detalle_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, cliente__usuario=request.user)
    return render(request, 'core/pedido_detalle.html', {'pedido': pedido})

@login_required(login_url='login')
def pedidos_view(request):
    pedidos = Pedido.objects.filter(cliente__usuario=request.user).order_by('-creado')
    return render(request, 'core/pedidos.html', {'pedidos': pedidos})
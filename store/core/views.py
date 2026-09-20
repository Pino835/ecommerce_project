from django.contrib.auth.models import User
from .models import Cliente, Producto, Categoria
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

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
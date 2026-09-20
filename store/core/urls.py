from django.urls import path
from .views import login_view, registro_view, hero_view, menu_view, perfil_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('', hero_view, name='hero'),
    path('menu/', menu_view, name='menu'),
    path('perfil/', perfil_view, name='perfil'),
    path('logout/', logout_view, name='logout'),
]
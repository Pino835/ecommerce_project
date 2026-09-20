# Ecommerce (portafolio)

Proyecto Django de práctica para portafolio personal. Catálogo de productos con autenticación
de usuarios y perfil de cliente. Aún no incluye carrito de compras ni checkout.

## Requisitos

- Python 3.13+

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Copia `store/.env.example` a `store/.env` y genera tu propia `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Ejecutar

```bash
cd store
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Estructura

Ver [CLAUDE.md](CLAUDE.md) para el detalle de la estructura del proyecto y el estado actual.

# CLAUDE.md

Guía para Claude Code al trabajar en este repositorio.

## Qué es este proyecto

Ecommerce de portafolio personal construido con **Django 6.0.5**. Es un proyecto en etapa temprana:
tiene catálogo de productos, autenticación de usuarios y perfil de cliente, pero **todavía no tiene
carrito de compras, pedidos ni checkout** (lo central de un ecommerce real). Tratarlo como un WIP.

## Estructura

```
ecommerce/
├── .venv/                  # entorno virtual (no tocar, no versionar)
└── store/                  # proyecto Django (carpeta raíz de trabajo real)
    ├── manage.py
    ├── db.sqlite3           # BD de desarrollo (no debe ir a git)
    ├── media/productos/     # imágenes de productos subidas por usuarios
    ├── store/                # paquete de configuración del proyecto
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py / asgi.py
    └── core/                 # única app Django del proyecto
        ├── models.py         # Cliente, Categoria, Producto
        ├── views.py          # login, registro, logout, hero, menu, perfil
        ├── urls.py
        ├── admin.py          # registro simple de los 3 modelos
        ├── tests.py          # vacío
        ├── migrations/
        ├── static/css/
        └── templates/
            ├── base.html
            ├── core/ (hero.html, menu.html, perfil.html)
            └── login/ (login.html, registro.html)
```

Todos los comandos de Django (`manage.py`) se ejecutan desde `store/`, no desde la raíz del repo.

## Modelos (core/models.py)

- **Cliente**: `OneToOneField` a `User` de Django. Guarda teléfono, provincia/cantón/distrito,
  dirección y fecha de registro. Se crea junto con el `User` en el registro (transacción atómica).
- **Categoria**: nombre único + descripción.
- **Producto**: FK a Categoria (`PROTECT`), nombre, descripción, precio, stock, imagen, disponible.

## Vistas (core/views.py)

Todas son function-based views, sin `Form`/`ModelForm` (validación manual vía `request.POST.get`).

- `login_view` / `logout_view` / `registro_view`: auth estándar de Django.
- `hero_view`: landing pública.
- `menu_view`: lista todas las categorías y productos (sin paginación ni filtrado).
- `perfil_view`: requiere login; usa `get_or_create` para el `Cliente` asociado.

## Estado actual y áreas conocidas de mejora

Este es el diagnóstico vigente a partir de una revisión inicial del proyecto. Mantenerlo actualizado
a medida que se resuelvan o aparezcan puntos nuevos.

### Resuelto
- `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` ahora se leen desde `store/.env` (no versionado; ver
  `store/.env.example`). `settings.py` incluye un loader mínimo de `.env` sin dependencias extra.
- `.gitignore` en la raíz excluye `.venv/`, `db.sqlite3`, `media/`, `__pycache__/` y `store/.env`.
- `requirements.txt` y `README.md` agregados en la raíz.
- Bug corregido: `registro_view` ahora renderiza `login/registro.html` (antes apuntaba a
  `core/registro.html`, que no existe) cuando el email ya está registrado.
- Repositorio git inicializado.

### Pendiente / prioridad alta
- Revisar si conviene migrar a `django-environ` si el proyecto crece (el loader actual de `.env`
  es deliberadamente simple).
- No hay tests (`core/tests.py` está vacío).

### Funcionalidad faltante (core de un ecommerce)
- No hay carrito de compras, ni modelo de `Pedido`/`OrderItem`, ni flujo de checkout/pago.
- `menu_view` no pagina ni filtra por categoría/búsqueda.
- No hay `Form`/`ModelForm` para registro ni edición de perfil (validación manual actualmente).

## Convenciones a seguir al modificar el código

- Mantener las vistas function-based salvo que se decida migrar explícitamente a CBVs.
- Preferir `ModelForm`/`Form` de Django para nuevas features de captura de datos, en vez de leer
  `request.POST` a mano.
- Los templates usan bloques `{% block title/styles/content/scripts %}` sobre `base.html`; seguir
  ese patrón para nuevas páginas.
- El código está en español (nombres de modelos, campos, vistas, mensajes); mantener consistencia
  de idioma en nuevo código de este proyecto.

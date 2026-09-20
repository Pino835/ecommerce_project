# CLAUDE.md

Guía para Claude Code al trabajar en este repositorio.

## Qué es este proyecto

Ecommerce de portafolio personal construido con **Django 6.0.5**. Tiene catálogo de productos,
autenticación de usuarios, perfil de cliente, carrito de compras y checkout con creación de
pedidos (sin pasarela de pago real todavía). Tratarlo como un WIP.

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
        ├── models.py         # Cliente, Categoria, Producto, Carrito, CarritoItem, Pedido, PedidoItem
        ├── views.py          # login, registro, logout, hero, menu, perfil, carrito, checkout, pedidos
        ├── urls.py
        ├── admin.py          # registro de modelos + inline de PedidoItem en Pedido
        ├── tests.py          # tests de carrito/checkout
        ├── migrations/
        ├── static/css/
        └── templates/
            ├── base.html
            ├── core/ (hero.html, menu.html, perfil.html, carrito.html, checkout.html,
            │         pedidos.html, pedido_detalle.html)
            └── login/ (login.html, registro.html)
```

Todos los comandos de Django (`manage.py`) se ejecutan desde `store/`, no desde la raíz del repo.

## Modelos (core/models.py)

- **Cliente**: `OneToOneField` a `User` de Django. Guarda teléfono, provincia/cantón/distrito,
  dirección y fecha de registro. Se crea junto con el `User` en el registro (transacción atómica).
- **Categoria**: nombre único + descripción.
- **Producto**: FK a Categoria (`PROTECT`), nombre, descripción, precio, stock, imagen, disponible.
- **Carrito**: `OneToOneField` a Cliente. Propiedad `total` (suma de subtotales de sus items).
- **CarritoItem**: FK a Carrito y Producto (únicos juntos), cantidad. Propiedad `subtotal`.
- **Pedido**: FK a Cliente (`PROTECT`), `estado` (choices: pendiente/pagado/enviado/entregado/
  cancelado), dirección de envío. Propiedad `total`.
- **PedidoItem**: FK a Pedido y Producto (`PROTECT`), cantidad y `precio_unitario` congelado al
  momento de la compra (no referencia el precio actual del producto). Propiedad `subtotal`.

## Vistas (core/views.py)

Todas son function-based views, sin `Form`/`ModelForm` (validación manual vía `request.POST.get`).

- `login_view` / `logout_view` / `registro_view`: auth estándar de Django.
- `hero_view`: landing pública.
- `menu_view`: lista todas las categorías y productos (sin paginación ni filtrado); cada producto
  tiene un botón "Agregar al carrito" si el usuario está autenticado.
- `perfil_view`: requiere login; usa `get_or_create` para el `Cliente` asociado.
- `_get_carrito`: helper interno que obtiene/crea Cliente y Carrito del usuario logueado.
- `carrito_view` / `carrito_agregar_view` / `carrito_eliminar_view`: gestión del carrito.
- `checkout_view`: valida stock, crea `Pedido` + `PedidoItem`s dentro de una transacción atómica,
  descuenta stock y vacía el carrito.
- `pedidos_view` / `pedido_detalle_view`: historial de pedidos del usuario logueado (el detalle
  verifica que el pedido pertenezca al usuario vía `cliente__usuario=request.user`).

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

- Carrito de compras y checkout implementados: modelos `Carrito`/`CarritoItem`/`Pedido`/`PedidoItem`,
  vistas de agregar/quitar/checkout, e historial de pedidos. Tests en `core/tests.py` cubren
  agregar al carrito, checkout exitoso (descuenta stock, vacía carrito) y checkout sin items.

### Pendiente / prioridad alta
- Revisar si conviene migrar a `django-environ` si el proyecto crece (el loader actual de `.env`
  es deliberadamente simple).
- No hay pasarela de pago real (el checkout crea el pedido en estado `pendiente` directamente).
- `menu_view` no pagina ni filtra por categoría/búsqueda.
- No hay `Form`/`ModelForm` para registro, perfil ni checkout (validación manual actualmente).
- No hay forma de editar cantidad en el carrito (solo agregar de a uno y quitar el item completo).

## Convenciones a seguir al modificar el código

- Mantener las vistas function-based salvo que se decida migrar explícitamente a CBVs.
- Preferir `ModelForm`/`Form` de Django para nuevas features de captura de datos, en vez de leer
  `request.POST` a mano.
- Los templates usan bloques `{% block title/styles/content/scripts %}` sobre `base.html`; seguir
  ese patrón para nuevas páginas.
- El código está en español (nombres de modelos, campos, vistas, mensajes); mantener consistencia
  de idioma en nuevo código de este proyecto.

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse
import json
import os
from django.conf import settings

def index(request):
    return HttpResponse("Vista del catálogo funcionando")

# Función auxiliar para leer el JSON
def cargar_datos():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'productos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def _productos_con_stock_temporal(request):
    productos = cargar_datos()
    stock_temporal = request.session.get('stock_temporal', {})
    for producto in productos:
        clave_producto = str(producto['id'])
        if clave_producto in stock_temporal:
            producto['stock'] = stock_temporal[clave_producto]
    return productos

def lista(request):
    productos = _productos_con_stock_temporal(request)
    busqueda = request.GET.get('q', request.GET.get('nombre', '')).strip()
    categoria_seleccionada = request.GET.get('categoria', '').strip()

    if busqueda:
        texto_busqueda = busqueda.casefold()
        productos = [
            producto for producto in productos
            if texto_busqueda in producto['nombre'].casefold()
        ]

    if categoria_seleccionada:
        categoria_normalizada = categoria_seleccionada.casefold()
        productos = [
            producto for producto in productos
            if producto['categoria'].casefold() == categoria_normalizada
        ]

    # Cálculos para el resumen
    todos_los_productos = _productos_con_stock_temporal(request)
    total_registros = len(productos)
    productos_con_stock = sum(1 for p in productos if p['stock'] > 0)
    categorias = sorted({p['categoria'] for p in todos_los_productos})
    
    contexto = {
        'productos': productos,
        'total_registros': total_registros,
        'productos_con_stock': productos_con_stock,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_seleccionada,
    }
    return render(request, 'catalogo/lista.html', contexto)

def admin_landing(request):
    if request.method == 'POST':
        messages.success(request, 'El título de la página se actualizó correctamente (simulación).')

    return render(request, 'catalogo/admin_landing.html')

def detalle(request, producto_id):
    productos = _productos_con_stock_temporal(request)
    # Buscar el producto por id
    producto = next((p for p in productos if p['id'] == producto_id), None)
    
    if not producto:
        raise Http404("Producto no encontrado en la ferretería") # Manejo de caso inexistente
        
    return render(request, 'catalogo/detalle.html', {'producto': producto})


def _obtener_carrito(request):
    return request.session.get('carrito', {})


def _guardar_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True


def agregar_al_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('detalle', producto_id=producto_id)

    producto = next(
        (producto for producto in _productos_con_stock_temporal(request) if producto['id'] == producto_id),
        None,
    )
    if not producto:
        raise Http404('Producto no encontrado en la ferretería')
    if producto['stock'] <= 0:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('detalle', producto_id=producto_id)

    try:
        cantidad_solicitada = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        cantidad_solicitada = 0

    if cantidad_solicitada < 1:
        messages.error(request, 'La cantidad debe ser al menos 1.')
        return redirect('detalle', producto_id=producto_id)

    carrito = _obtener_carrito(request)
    clave_producto = str(producto_id)
    item = carrito.get(clave_producto, {
        'id': producto['id'],
        'nombre': producto['nombre'],
        'precio': producto['precio'],
        'cantidad': 0,
    })
    cantidad_total = item['cantidad'] + cantidad_solicitada
    if cantidad_total <= producto['stock']:
        item['cantidad'] = cantidad_total
        carrito[clave_producto] = item
        _guardar_carrito(request, carrito)
        messages.success(request, f"Se añadieron {cantidad_solicitada} unidad(es) de {producto['nombre']} al carrito.")
    else:
        disponibles = max(producto['stock'] - item['cantidad'], 0)
        messages.warning(request, f'Solo puedes añadir {disponibles} unidad(es) más de este producto.')
    return redirect('detalle', producto_id=producto_id)


def carrito(request):
    items = _items_con_subtotales(request)
    total = sum(item['precio'] * item['cantidad'] for item in items)
    return render(request, 'catalogo/carrito.html', {'items_carrito': items, 'total_carrito': total})


def _items_con_subtotales(request):
    items = []
    for item in _obtener_carrito(request).values():
        item_con_subtotal = dict(item)
        item_con_subtotal['subtotal'] = item['precio'] * item['cantidad']
        items.append(item_con_subtotal)
    return items


def vaciar_carrito(request):
    if request.method == 'POST':
        request.session.pop('carrito', None)
        messages.success(request, 'El carrito temporal fue vaciado.')
    return redirect('carrito')


def actualizar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = _obtener_carrito(request)
        clave_producto = str(producto_id)
        if clave_producto not in carrito:
            messages.error(request, 'El producto no está en el carrito.')
            return redirect('carrito')

        producto = next(
            (producto for producto in _productos_con_stock_temporal(request) if producto['id'] == producto_id),
            None,
        )
        try:
            cantidad = int(request.POST.get('cantidad', 0))
        except (TypeError, ValueError):
            cantidad = 0

        if cantidad <= 0:
            carrito.pop(clave_producto, None)
            _guardar_carrito(request, carrito)
            messages.info(request, 'Producto eliminado del carrito.')
        elif not producto:
            messages.error(request, 'Producto no encontrado en la ferretería.')
        elif cantidad > producto['stock']:
            messages.warning(request, f"Solo hay {producto['stock']} unidad(es) disponibles.")
        else:
            carrito[clave_producto]['cantidad'] = cantidad
            _guardar_carrito(request, carrito)
            messages.success(request, 'Cantidad actualizada.')
    return redirect('carrito')


def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = _obtener_carrito(request)
        if carrito.pop(str(producto_id), None) is not None:
            _guardar_carrito(request, carrito)
            messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        contrasena = request.POST.get('contrasena', '')
        usuario_registrado = request.session.get('usuario_registrado')
        if (
            usuario
            and usuario_registrado
            and usuario == usuario_registrado.get('usuario')
            and contrasena == usuario_registrado.get('contrasena')
        ):
            request.session['usuario_ficticio'] = usuario
            messages.success(request, f'Bienvenido/a, {usuario}.')
            return redirect(request.POST.get('next') or 'carrito')
        messages.error(request, 'El usuario o la contraseña no son válidos.')
    return render(request, 'catalogo/login.html', {'modo': 'login'})


def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        contrasena = request.POST.get('contrasena', '')
        confirmacion = request.POST.get('confirmacion', '')
        if not usuario or not contrasena:
            messages.error(request, 'Completa el usuario y la contraseña.')
        elif contrasena != confirmacion:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            request.session['usuario_registrado'] = {
                'usuario': usuario,
                'contrasena': contrasena,
            }
            request.session['usuario_ficticio'] = usuario
            messages.success(request, f'Cuenta simulada creada para {usuario}.')
            return redirect(request.POST.get('next') or 'lista')
    return render(request, 'catalogo/login.html', {'modo': 'registro'})


def logout(request):
    request.session.pop('usuario_ficticio', None)
    messages.success(request, 'La sesión simulada fue cerrada.')
    return redirect('lista')


def comprar(request, producto_id):
    if not request.session.get('usuario_ficticio'):
        messages.info(request, 'Inicia sesión para comprar este producto.')
        return redirect(f"{reverse('login')}?next={reverse('comprar', args=[producto_id])}")

    if request.method != 'POST':
        return redirect('detalle', producto_id=producto_id)

    producto = next(
        (producto for producto in _productos_con_stock_temporal(request) if producto['id'] == producto_id),
        None,
    )
    if not producto:
        raise Http404('Producto no encontrado en la ferretería')
    if producto['stock'] <= 0:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('lista')

    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except (TypeError, ValueError):
        cantidad = 1
    if cantidad > producto['stock']:
        messages.warning(request, f"Solo hay {producto['stock']} unidad(es) disponibles.")
        return redirect('detalle', producto_id=producto_id)

    carrito = _obtener_carrito(request)
    carrito[str(producto_id)] = {
        'id': producto['id'],
        'nombre': producto['nombre'],
        'precio': producto['precio'],
        'cantidad': cantidad,
        'imagen_url': producto.get('imagen_url', ''),
    }
    _guardar_carrito(request, carrito)
    return redirect('checkout')


def pedido_confirmado(request):
    items = request.session.get('ultimo_pedido', [])
    total = sum(item['subtotal'] for item in items)
    return render(request, 'catalogo/pedido_confirmado.html', {
        'items_carrito': items,
        'total_carrito': total,
    })


def checkout(request):
    if not request.session.get('usuario_ficticio'):
        messages.info(request, 'Inicia sesión para finalizar la compra simulada.')
        return redirect(f"{reverse('login')}?next={reverse('checkout')}")

    items = _items_con_subtotales(request)
    if not items:
        messages.info(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    total = sum(item['precio'] * item['cantidad'] for item in items)
    if request.method == 'POST':
        stock_temporal = request.session.get('stock_temporal', {})
        for item in items:
            clave_producto = str(item['id'])
            stock_actual = next(
                (producto['stock'] for producto in _productos_con_stock_temporal(request) if producto['id'] == item['id']),
                0,
            )
            if item['cantidad'] > stock_actual:
                messages.error(request, f"El stock de {item['nombre']} cambió y ya no alcanza para completar el pedido.")
                return redirect('carrito')
            stock_temporal[clave_producto] = stock_actual - item['cantidad']

        request.session['stock_temporal'] = stock_temporal
        request.session['ultimo_pedido'] = items
        request.session.pop('carrito', None)
        messages.success(request, 'Pedido confirmado correctamente (simulación).')
        return redirect('pedido_confirmado')

    return render(request, 'catalogo/checkout.html', {'items_carrito': items, 'total_carrito': total})


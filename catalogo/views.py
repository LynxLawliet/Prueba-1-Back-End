from django.shortcuts import render
from django.http import HttpResponse, Http404
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

def lista(request):
    productos = cargar_datos()
    return render(request, 'catalogo/lista.html', {'productos': productos})

def detalle(request, producto_id):
    productos = cargar_datos()
    # Buscar el producto por id
    producto = next((p for p in productos if p['id'] == producto_id), None)
    
    if not producto:
        raise Http404("Producto no encontrado en la ferretería") # Manejo de caso inexistente
        
    return render(request, 'catalogo/detalle.html', {'producto': producto})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Venta
from django.conf import settings
lista_ventas = []
cb = [1]
TOTAL = [0.0]

# Create your views here.
def home(request):
    return render(request, 'cajero/home.html')

def login(request):
    return render(request, 'cajero/login.html')

def productos(request):
    productos = Producto.objects.all()
    data = {
        'productos':productos
    }
    return render(request, 'cajero/productos.html', data)

def ventas(request):
    class Venta_():
        def __init__(self, nombre, precio, cantidad, total):
            self.nombre = nombre
            self.precio = precio
            self.cantidad = cantidad
            self.total = total
    total = 0
    counter = 1
    if request.method == "POST":
        cod = request.POST["codigo"]
        cant = float(request.POST["cantidad"])
        producto = get_object_or_404(Producto, codigo = cod)
        cant_updated = int(producto.cantidad - cant)
        if cant_updated >= 0:
            Producto.objects.filter(codigo=cod).update(cantidad = cant_updated)
            total = cant * float(producto.precio)
            lista_ventas.append(Venta_(producto.nombre, producto.precio, int(cant), total,))
            TOTAL[0] += total
        data = {
            'p':producto,
            'totall': total,
            'disp': cant_updated,
            'cant': int(cant),
            'list_ven': lista_ventas,
            'TOTAL': TOTAL[0]
        }
        return render(request, 'cajero/ventas.html', data)
    return render(request, 'cajero/ventas.html')

def agregar_venta(request):
    bol = 'BO-'
    bol += str(cb[0])
    cb[0] += 1
    current_user = request.user
    # print()
    venta_t = Venta(id_user=current_user, boleta=bol, total = TOTAL[0])
    venta_t.save()
    lista_ventas.clear()
    TOTAL[0] = 0.0
    return render(request, 'cajero/ventas.html')
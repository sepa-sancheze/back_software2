from django.db import models
from usuario.models import Usuario
from productos.models import Producto
from sucursal.models import Sucursal

# Create your models here.
class Ventas(models.Model):
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length = 20)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
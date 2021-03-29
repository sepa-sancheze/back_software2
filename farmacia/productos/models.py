from django.db import models
from sucursal.models import Sucursal

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)

class Medida(models.Model):
    nombre = models.CharField(max_length = 25)
    unidad_medida = models.CharField(max_length = 15)
    dimension = models.DecimalField(max_digits = 5, decimal_places = 2)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio_compra = models.DecimalField(max_digits = 5, decimal_places = 2)
    precio_venta = models.DecimalField(max_digits = 5, decimal_places = 2)
    descripcion = models.CharField(max_length = 150)
    categoria = models.ManyToManyField(Categoria)
    medida = models.ManyToManyField(Medida)

class ExistenciasProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete = models.CASCADE)
    maximo = models.IntegerField()
    minimo = models.IntegerField()
    existencias = models.IntegerField()
    activo = models.BooleanField(default = True)

class LotesProducto(models.Model):
    numero_lote = models.CharField(max_length = 20)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    existencias = models.IntegerField()
    fecha_vencimiento = models.DateField(auto_now=False, auto_now_add=False)
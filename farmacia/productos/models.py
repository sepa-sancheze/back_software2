from django.db import models

# Create your models here.
class Medida(models.Model):
    nombre = models.CharField(max_length = 25)
    unidad_medida = models.CharField(max_length = 15)
    dimension = models.DecimalField(max_digits = 5, decimal_places = 2)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio_compra = models.DecimalField(max_digits = 5, decimal_places = 2)
    precio_venta = models.DecimalField(max_digits = 5, decimal_places = 2)
    descripcion = models.CharField(max_length = 150)
    medida = models.ManyToManyField(Medida)
    existencias = models.IntegerField()
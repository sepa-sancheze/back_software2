from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio_compra = models.DecimalField(max_digits = 5, decimal_places = 2)
    precio_venta = models.DecimalField(max_digits = 5, decimal_places = 2)
    descripcion = models.CharField(max_length = 150)
    existencias = models.IntegerField()
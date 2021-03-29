from django.db import models

# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length = 50)
    direccion = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 10)

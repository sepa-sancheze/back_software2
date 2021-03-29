from django.db import models

# Create your models here.
class Rol(models.Model):
    nombre = models.CharField(max_length=100)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    rol = models.ForeignKey(Rol, on_delete = models.CASCADE)
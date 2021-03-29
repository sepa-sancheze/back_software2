from django.contrib import admin
from .models import Ventas, DetalleVenta

# Register your models here.
admin.site.register(Ventas)
admin.site.register(DetalleVenta)
from django.contrib import admin
from .models import Producto, ExistenciasProducto, Categoria, Medida

# Register your models here.
admin.site.register(Producto)
admin.site.register(ExistenciasProducto)
admin.site.register(Categoria)
admin.site.register(Medida)
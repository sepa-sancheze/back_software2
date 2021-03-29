from rest_framework import serializers
from .models import Producto, Medida

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_compra', 'precio_venta', 'medida', 'descripcion', 'categoria', 'existencias']
        depth = 1

class ProductoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_compra', 'precio_venta','medida', 'descripcion', 'categoria', 'existencias']

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = ['id', 'nombre', 'unidad_medida', 'dimension']
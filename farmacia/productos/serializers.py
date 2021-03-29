from rest_framework import serializers
from .models import Producto, ExistenciasProducto, Categoria, Medida, LotesProducto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_compra', 'precio_venta', 'medida', 'descripcion', 'categoria']
        depth = 1

class ProductoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_compra', 'precio_venta','medida', 'descripcion', 'categoria']

class ExistenciasProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistenciasProducto
        fields = ['producto', 'sucursal', 'existencias', 'maximo', 'minimo', 'activo']
        depth = 2

class ExistenciasProductoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = ExistenciasProducto
        fields = ['producto', 'sucursal', 'existencias', 'maximo', 'minimo', 'activo']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = ['id', 'nombre', 'unidad_medida', 'dimension']

class LotesProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotesProducto
        fields = ['numero_lote', 'producto', 'sucursal', 'existencias', 'fecha_vencimiento']
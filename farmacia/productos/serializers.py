from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_compra', 'precio_venta', 'categoria', 'existencias']
        depth = 1
    
class ProductoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_compra', 'precio_venta',' descripcion' 'existencias']
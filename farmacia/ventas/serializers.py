from rest_framework import serializers
from .models import Ventas, DetalleVenta

class VentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = ['id', 'fecha', 'usuario', 'total', 'estado']
        depth = 1

class VentasSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = ['id', 'fecha', 'usuario', 'total', 'estado']

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'venta', 'producto', 'cantidad', 'subtotal']
        depth = 1

class DetalleVentaSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'venta', 'producto', 'cantidad', 'subtotal']
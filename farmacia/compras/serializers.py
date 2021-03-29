from rest_framework import serializers
from .models import Compras, DetalleCompra

class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = ['id', 'fecha', 'usuario', 'total', 'estado', 'sucursal']
        depth = 1

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ['id', 'compra', 'producto', 'cantidad', 'subtotal']
        depth = 2

class DetalleCompraSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ['id', 'compra', 'producto', 'cantidad', 'subtotal']

class ComprasSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = ['id', 'fecha', 'usuario', 'total', 'estado', 'sucursal']
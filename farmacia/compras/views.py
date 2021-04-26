from .models import Compras, DetalleCompra
from productos.models import Producto
from productos.serializers import ProductoSerializer
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ComprasSerializer, DetalleCompraSerializer, ComprasSerializerPost, DetalleCompraSerializerPost
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from django.http import Http404

class ComprasLista(APIView):

    def get(self, request, format = None):
        objeto = Compras.objects.all()
        serializer = ComprasSerializer(objeto, many = True)
        return Response(serializer.data)
    
    def post(self, request, format = None):
        serializer = ComprasSerializerPost(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ComprasUnico(APIView):

    def get_objecto(self, pk):
        try:
            return Compras.objects.get(pk = pk)
        except Compras.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        serializer = ComprasSerializer(objeto)
        return Response(serializer.data)
    
    def put(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        serializer = ComprasSerializer(objeto, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        objeto.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class DetalleCompraLista(APIView):

    def get(self, request, format = None):
        objeto = DetalleCompra.objects.all()
        serializer = DetalleCompraSerializer(objeto, many = True)
        return Response(serializer.data)
    
    def post(self, request, format = None):
        cantidad = request.data['cantidad']
        id_producto = request.data['producto']
        precio_producto = Producto.objects.filter(id = id_producto).values('precio_compra')[0]['precio_compra']
        subtotal = cantidad * precio_producto            
        request.data['subtotal'] = subtotal
        
        serializer = DetalleCompraSerializerPost(data = request.data)
        if serializer.is_valid():    
            existencias_producto_actual = Producto.objects.filter(id = id_producto).values('existencias')[0]['existencias']

            # Actualizar total de la venta
            compra_actualizar_object = Compras.objects.filter(id = request.data['compra']).first()
            compra_actualizar = model_to_dict(compra_actualizar_object)['total'] + subtotal

            update_data = {'total': compra_actualizar}
            serializer_total_compra = ComprasSerializerPost(compra_actualizar_object, data=update_data, partial = True)
            if serializer_total_compra.is_valid():
                serializer_total_compra.save()
            else:
                return Response(serializer_total_compra.errors, status = status.HTTP_400_BAD_REQUEST)            
            
            # Descontar productos <-> Terminado
            productos_descontar_object = Producto.objects.filter(producto = id_producto).first()
            productos_descontar = model_to_dict(productos_descontar_object)['existencias'] + cantidad
            update_data = {'existencias': productos_descontar}
            serializer_total_descontar = ProductoSerializer(productos_descontar_object, data=update_data, partial = True)
            if serializer_total_descontar.is_valid():
                serializer_total_descontar.save()
            else:
                return Response(serializer_total_descontar.errors, status = status.HTTP_400_BAD_REQUEST)            

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DetalleCompraUnico(APIView):

    def get_objecto(self, pk):
        try:
            return DetalleCompra.objects.get(pk = pk)
        except DetalleCompra.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        objeto = DetalleCompra.objects.filter(compra = pk)
        serializer = DetalleCompraSerializer(objeto, many = True)
        return Response(serializer.data)
    
    def delete(self, request, pk, format = None):
        objeto = self.get_objecto(pk)

        # Descontar de la compra
        id_compra_object = DetalleCompra.objects.filter(id = pk).first()
        id_compra = model_to_dict(id_compra_object)['compra']
        
        subtotal_detalle_object = DetalleCompra.objects.filter(id = pk).first()
        subtotal_detalle = model_to_dict(subtotal_detalle_object)['subtotal']
        
        compra_object = Compras.objects.filter(id = id_compra).first()

        total_compra = model_to_dict(compra_object)['total'] - subtotal_detalle
        update_data = {'total': total_compra}

        serializer_total_compra = ComprasSerializer(compra_object, data=update_data, partial = True)

        if serializer_total_compra.is_valid():
            serializer_total_compra.save()
        else:
            return Response(serializer_total_compra.errors, status = status.HTTP_400_BAD_REQUEST)            
        
        # Retornar existencias
        existencias = model_to_dict(objeto)['cantidad']
        id_producto = model_to_dict(objeto)['producto']

        producto_object = Producto.objects.filter(producto = id_producto).first()
        existencias_final = model_to_dict(producto_object)['existencias'] - existencias
        existencias_totales = {'existencias': existencias_final}

        serializer_nuevas_existencias = ProductoSerializer(producto_object, data = existencias_totales, partial = True)
        if serializer_nuevas_existencias.is_valid():
            serializer_nuevas_existencias.save()
        else:
            return Response(serializer_nuevas_existencias.errors, status = status.HTTP_400_BAD_REQUEST)

        objeto.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
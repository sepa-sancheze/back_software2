from .models import Ventas, DetalleVenta
from productos.models import Producto
from productos.serializers import ProductoSerializer
from rest_framework import status
from rest_framework.views import APIView
from .serializers import VentasSerializer, DetalleVentaSerializer, VentasSerializerPost, DetalleVentaSerializerPost
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from django.http import Http404

class VentasLista(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        if request.user.has_perm('ventas.view_ventas'):
            objeto = Ventas.objects.all()
            serializer = VentasSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def post(self, request, format = None):
        if request.user.has_perm('ventas.add_ventas'):
            serializer = VentasSerializerPost(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class VentasUnico(APIView):

    permission_classes = (IsAuthenticated, )

    def get_objecto(self, pk):
        try:
            return Ventas.objects.get(pk = pk)
        except Ventas.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        if request.user.has_perm('ventas.view_ventas'):
            objeto = self.get_objecto(pk)
            serializer = VentasSerializer(objeto)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk, format = None):
        if request.user.has_perm('ventas.change_ventas'):
            objeto = self.get_objecto(pk)
            serializer = VentasSerializer(objeto, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('ventas.delete_ventas'):
            objeto = self.get_objecto(pk)
            objeto.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class DetalleVentaLista(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        if request.user.has_perm('ventas.view_detalleventa'):
            objeto = DetalleVenta.objects.all()
            serializer = DetalleVentaSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def post(self, request, format = None):
        if request.user.has_perm('ventas.add_detalleventa'):
            
            cantidad = request.data['cantidad']
            id_producto = request.data['producto']
            precio_producto = Producto.objects.filter(id = id_producto).values('precio_venta')[0]['precio_venta']
            subtotal = cantidad * precio_producto            
            request.data['subtotal'] = subtotal
            
            serializer = DetalleVentaSerializerPost(data = request.data)
            if serializer.is_valid():    
                existencias_producto_actual = Producto.objects.filter(id = id_producto).values('existencias')[0]['existencias']

                if existencias_producto_actual >= cantidad:
                    #request.data.update({'subtotal': subtotal})

                    # Actualizar total de la venta
                    venta_actualizar_object = Ventas.objects.filter(id = request.data['venta']).first()
                    venta_actualizar = model_to_dict(venta_actualizar_object)['total'] + subtotal

                    update_data = {'total': venta_actualizar}
                    serializer_total_venta = VentasSerializerPost(venta_actualizar_object, data=update_data, partial = True)
                    if serializer_total_venta.is_valid():
                        serializer_total_venta.save()
                    else:
                        return Response(serializer_total_venta.errors, status = status.HTTP_400_BAD_REQUEST)            
                    
                    # Descontar productos <-> Terminado
                    productos_descontar_object = Producto.objects.filter(producto = id_producto).first()
                    productos_descontar = model_to_dict(productos_descontar_object)['existencias'] - cantidad
                    update_data = {'existencias': productos_descontar}
                    serializer_total_descontar = ProductoSerializer(productos_descontar_object, data=update_data, partial = True)
                    if serializer_total_descontar.is_valid():
                        serializer_total_descontar.save()
                    else:
                        return Response(serializer_total_descontar.errors, status = status.HTTP_400_BAD_REQUEST)            

                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    return Response(status = status.HTTP_406_NOT_ACCEPTABLE)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class DetalleVentaUnico(APIView):

    permission_classes = (IsAuthenticated, )

    def get_objecto(self, pk):
        try:
            return DetalleVenta.objects.get(pk = pk)
        except DetalleVenta.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        if request.user.has_perm('ventas.view_detalleventa'):
            objeto = DetalleVenta.objects.filter(venta = pk)
            serializer = DetalleVentaSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('ventas.delete_ventas'):
            objeto = self.get_objecto(pk)

            # Descontar de la venta
            id_venta_object = DetalleVenta.objects.filter(id = pk).first()
            id_venta = model_to_dict(id_venta_object)['venta']
            
            subtotal_detalle_object = DetalleVenta.objects.filter(id = pk).first()
            subtotal_detalle = model_to_dict(subtotal_detalle_object)['subtotal']
            
            venta_object = Ventas.objects.filter(id = id_venta).first()

            total_venta = model_to_dict(venta_object)['total'] - subtotal_detalle
            update_data = {'total': total_venta}

            serializer_total_venta = VentasSerializer(venta_object, data=update_data, partial = True)

            if serializer_total_venta.is_valid():
                serializer_total_venta.save()
            else:
                return Response(serializer_total_venta.errors, status = status.HTTP_400_BAD_REQUEST)            
            
            # Retornar existencias
            existencias = model_to_dict(objeto)['cantidad']
            id_producto = model_to_dict(objeto)['producto']

            producto_object = Producto.objects.filter(producto = id_producto).first()
            existencias_final = model_to_dict(producto_object)['existencias'] + existencias
            existencias_totales = {'existencias': existencias_final}

            serializer_nuevas_existencias = ProductoSerializer(producto_object, data = existencias_totales, partial = True)
            if serializer_nuevas_existencias.is_valid():
                serializer_nuevas_existencias.save()
            else:
                return Response(serializer_nuevas_existencias.errors, status = status.HTTP_400_BAD_REQUEST)

            objeto.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)            

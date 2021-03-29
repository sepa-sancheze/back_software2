from .models import Producto, Medida
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import ProductoSerializer, MedidaSerializer, ProductoSerializerPost
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.db.models import Q

class ProductoLista(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        if request.user.has_perm('producto.view_producto'):
            objeto = Producto.objects.all()
            serializer = ProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request, format = None):
        if request.user.has_perm('producto.add_producto'):
            serializer = ProductoSerializerPost(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class ProductoUnico(APIView):

    permission_classes = (IsAuthenticated, )

    def get_objecto(self, pk):
        try:
            return Producto.objects.get(pk = pk)
        except Producto.DoesNotExist:
            raise Http404
    
    def get(self, request, format = None, *args, **kwargs):
        if request.user.has_perm('producto.view_producto'):
            if kwargs.get("pk") == None:
                objeto = Producto.objects.filter(nombre = kwargs.get("name"))
                serializer = ProductoSerializer(objeto, many = True)
                return Response(serializer.data)
            else:
                objeto = Producto.objects.filter(id = kwargs.get("pk"))
                serializer = ProductoSerializer(objeto, many = True)
                return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk, format = None):
        if request.user.has_perm('producto.change_producto'):
            objeto = self.get_objecto(pk)
            serializer = ProductoSerializerPost(objeto, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('producto.delete_producto'):
            objeto = self.get_objecto(pk)
            objeto.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class MedidasLista(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Medida.objects.all()
    serializer_class = MedidaSerializer

class MedidaUnico(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Medida.objects.all()
    serializer_class = MedidaSerializer

from .models import Producto
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import ProductoSerializer, ProductoSerializerPost
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.db.models import Q

class ProductoLista(APIView):

    def get(self, request, format = None):
        objeto = Producto.objects.all()
        serializer = ProductoSerializer(objeto, many = True)
        return Response(serializer.data)
        
    
    def post(self, request, format = None):
        serializer = ProductoSerializerPost(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductoUnico(APIView):

    def get_objecto(self, pk):
        try:
            return Producto.objects.get(pk = pk)
        except Producto.DoesNotExist:
            raise Http404
    
    def get(self, request, format = None, *args, **kwargs):
        if kwargs.get("pk") == None:
            objeto = Producto.objects.filter(nombre = kwargs.get("name"))
            serializer = ProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            objeto = Producto.objects.filter(id = kwargs.get("pk"))
            serializer = ProductoSerializer(objeto, many = True)
            return Response(serializer.data)
    
    def put(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        serializer = ProductoSerializerPost(objeto, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        objeto.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

from .models import Producto, ExistenciasProducto, Categoria, Medida
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import ProductoSerializer, ExistenciasProductoSerializer, CategoriaSerializer, MedidaSerializer, ProductoSerializerPost, ExistenciasProductoSerializerPost
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

class ExistenciasLista(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        if request.user.has_perm('producto.view_existenciasproducto'):
            objeto = ExistenciasProducto.objects.all()
            serializer = ExistenciasProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request, format = None):
        if request.user.has_perm('producto.add_existenciasproducto'):
            serializer = ExistenciasProductoSerializerPost(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class ExistenciasUnico(APIView):
    permission_classes = (IsAuthenticated, )

    def get_objecto(self, pk):
        try:
            return ExistenciasProducto.objects.get(producto = pk)
        except ExistenciasProducto.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        if request.user.has_perm('producto.view_existenciasproducto'):
            objeto = ExistenciasProducto.objects.filter(producto = pk)
            serializer = ExistenciasProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk, format = None):
        if request.user.has_perm('producto.change_existenciasproducto'):
            objeto = self.get_objecto(pk)
            serializer = ExistenciasProductoSerializer(objeto, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('producto.delete_existenciasproducto'):
            objeto = self.get_objecto(pk)
            objeto.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class CategoriaLista(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        if request.user.has_perm('producto.view_categoria'):
            objeto = Categoria.objects.all()
            serializer = CategoriaSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request, format = None):
        if request.user.has_perm('producto.add_categoria'):
            serializer = CategoriaSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class CategoriaUnica(APIView):

    permission_classes = (IsAuthenticated, )

    def get_objecto(self, pk):
        try:
            return Categoria.objects.get(pk = pk)
        except Categoria.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        if request.user.has_perm('producto.view_categoria'):
            objeto = self.get_objecto(pk)
            serializer = CategoriaSerializer(objeto)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk, format = None):
        if request.user.has_perm('producto.change_categoria'):
            objeto = self.get_objecto(pk)
            serializer = CategoriaSerializer(objeto, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('producto.delete_categoria'):
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

class ProductoPorCategoria(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, name ,format = None):
        if request.user.has_perm('producto.view_producto'):
            indicador = Categoria.objects.filter(nombre__icontains = name).values('id')
            id = indicador[0]['id']
            #objeto = ExistenciasProducto.objects.all()
            objeto = Producto.objects.filter(categoria = id)
            serializer = ProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class ExistenciasProductoSucursal(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format = None):
        if request.user.has_perm('producto.view_existenciasproducto'):
            objeto = ExistenciasProducto.objects.all().filter(sucursal = pk)
            serializer = ExistenciasProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class ProductoNotSucursal(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format = None):
        if request.user.has_perm('producto.view_existenciasproducto'):
            productos = ExistenciasProducto.objects.filter(sucursal = pk).values('producto')
            objeto = Producto.objects.exclude(id__in = productos)
            serializer = ProductoSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class ProductoPorSucursal(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format = None):
        if request.user.has_perm('producto.view_existenciasproducto'):
            productos = ExistenciasProducto.objects.filter(sucursal = pk).values('producto')
            objeto = Producto.objects.filter(id__in = productos).values()
            obj = []
            for a in objeto:
                obj.append(a)
            return Response(obj)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
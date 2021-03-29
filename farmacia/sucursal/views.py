from .models import Sucursal
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SucursalSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.http import Http404

class SucursalLista(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        if request.user.has_perm('sucursal.view_sucursal'):
            objeto = Sucursal.objects.all()
            serializer = SucursalSerializer(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request, format = None):
        if request.user.has_perm('sucursal.add_sucursal'):
            serializer = SucursalSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.erros, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class sucursalUnico(APIView):

    permission_classes = (IsAuthenticated, )

    def get_objecto(self, pk):
        try:
            return Sucursal.objects.get(pk = pk)
        except Sucursal.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        if request.user.has_perm('sucursal.view_sucursal'):
            objeto = self.get_objecto(pk)
            serializer = SucursalSerializer(objeto)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk, format = None):
        if request.user.has_perm('sucursal.change_sucursal'):
            objeto = self.get_objecto(pk)
            serializer = SucursalSerializer(objeto, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('sucursal.delete_sucursal'):
            objeto = self.get_objecto(pk)
            objeto.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

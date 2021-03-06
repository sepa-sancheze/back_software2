from .models import Usuario
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import UsuarioSerializer, UsuarioSerializerPut
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.http import Http404

class UsuariosLista(APIView):

    def get(self, request, format = None):
        objeto = Usuario.objects.all()
        serializer = UsuarioSerializer(objeto, many = True)
        return Response(serializer.data)
        
    
    def post(self, request, format = None):
        serializer = UsuarioSerializer(data = request.data)
        if serializer.is_valid():
            usuario = request.data['usuario']
            password = request.data['password']
            # Crear usuario en django
            user = User.objects.create_user(usuario, password = password)
            user.save()
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UsuarioUnico(APIView):

    def get_objecto(self, pk):
        try:
            return Usuario.objects.get(pk = pk)
        except Usuario.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        serializer = UsuarioSerializerGet(objeto)
        return Response(serializer.data)
    
    def put(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        serializer = UsuarioSerializerPut(objeto, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        objeto = self.get_objecto(pk)
        objeto.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

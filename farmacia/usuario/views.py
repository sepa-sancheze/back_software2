from .models import Usuario, Rol
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import UsuarioSerializer, RolSerializer, UsuarioSerializerGet, UsuarioSerializerPut
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.http import Http404

class UsuariosLista(APIView):

    def get(self, request, format = None):
        if request.user.has_perm('usuario.view_usuario'):
            objeto = Usuario.objects.all()
            serializer = UsuarioSerializerGet(objeto, many = True)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    
    def post(self, request, format = None):
        if request.user.has_perm('usuario.add_usuario'):
            serializer = UsuarioSerializer(data = request.data)
            if serializer.is_valid():
                usuario = request.data['usuario']
                password = request.data['password']
                rol = request.data['rol']
                # Crear usuario en django
                user = User.objects.create_user(usuario, password = password)
                user.save()
                if rol == 1:
                    my_group = Group.objects.get(name='Nivel 1') 
                    my_group.user_set.add(user)
                elif rol == 2:
                    my_group = Group.objects.get(name='Nivel 2') 
                    my_group.user_set.add(user)
                elif rol == 3:
                    my_group = Group.objects.get(name='Nivel 3') 
                    my_group.user_set.add(user)

                
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class UsuarioUnico(APIView):

    def get_objecto(self, pk):
        try:
            return Usuario.objects.get(pk = pk)
        except Usuario.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        if request.user.has_perm('usuario.view_usuario'):
            objeto = self.get_objecto(pk)
            serializer = UsuarioSerializerGet(objeto)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def put(self, request, pk, format = None):
        if request.user.has_perm('usuario.change_usuario'):
            objeto = self.get_objecto(pk)
            serializer = UsuarioSerializerPut(objeto, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format = None):
        if request.user.has_perm('usuario.delete_usuario'):
            objeto = self.get_objecto(pk)
            objeto.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

class RolLista(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class RolUnico(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import UsuariosLista, UsuarioUnico, RolLista, RolUnico


urlpatterns = [
    path('', UsuariosLista.as_view()),
    path('<int:pk>', UsuarioUnico.as_view()),
    path('rol/', RolLista.as_view()),
    path('rol/<int:pk>/', RolUnico.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
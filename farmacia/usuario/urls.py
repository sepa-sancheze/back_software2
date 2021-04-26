from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import UsuariosLista, UsuarioUnico


urlpatterns = [
    path('', UsuariosLista.as_view()),
    path('<int:pk>', UsuarioUnico.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
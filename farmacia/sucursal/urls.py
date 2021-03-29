from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import SucursalLista, sucursalUnico


urlpatterns = [
    path('', SucursalLista.as_view()),
    path('<int:pk>', sucursalUnico.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
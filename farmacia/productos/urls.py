from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import ProductoLista, ProductoUnico, ExistenciasLista, ExistenciasUnico, CategoriaUnica, CategoriaLista, MedidasLista, MedidaUnico, ProductoPorCategoria, ExistenciasProductoSucursal, ProductoNotSucursal, ProductoPorSucursal


urlpatterns = [
    path('', ProductoLista.as_view()),
    path('<int:pk>', ProductoUnico.as_view()),
    path('<str:name>', ProductoUnico.as_view()),
    path('sucursal/<int:pk>', ExistenciasProductoSucursal.as_view()),
    path('existencias/', ExistenciasLista.as_view()),
    path('existencias/<int:pk>', ExistenciasUnico.as_view()),
    path('existencias/categoria/<str:name>', ProductoPorCategoria.as_view()),
    path('categoria/', CategoriaLista.as_view()),
    path('categoria/<int:pk>', CategoriaUnica.as_view()),
    path('medidas/', MedidasLista.as_view()),
    path('medidas/<int:pk>', MedidaUnico.as_view()),
    path('not_sucursal/<int:pk>', ProductoNotSucursal.as_view()),
    path('info/<int:pk>', ProductoPorSucursal.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
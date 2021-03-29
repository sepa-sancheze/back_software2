from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import ComprasLista, ComprasUnico, DetalleCompraLista, DetalleCompraUnico, ComprasSucural


urlpatterns = [
    path('', ComprasLista.as_view()),
    path('<int:pk>/', ComprasUnico.as_view()),
    path('sucursal/<int:pk>/', ComprasSucural.as_view()),
    path('detalle_compra/', DetalleCompraLista.as_view()),
    path('detalle_compra/<int:pk>/', DetalleCompraUnico.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import VentasLista, DetalleVentaLista, VentasUnico, DetalleVentaUnico, VentasSucural


urlpatterns = [
    path('', VentasLista.as_view()),
    path('<int:pk>/', VentasUnico.as_view()),
        path('sucursal/<int:pk>/', VentasSucural.as_view()),
    path('detalle_venta/', DetalleVentaLista.as_view()),
    path('detalle_venta/<int:pk>/', DetalleVentaUnico.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
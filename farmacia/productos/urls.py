from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import ProductoLista, ProductoUnico, MedidasLista, MedidaUnico


urlpatterns = [
    path('', ProductoLista.as_view()),
    path('<int:pk>', ProductoUnico.as_view()),
    path('<str:name>', ProductoUnico.as_view()),
    path('medidas/', MedidasLista.as_view()),
    path('medidas/<int:pk>', MedidaUnico.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
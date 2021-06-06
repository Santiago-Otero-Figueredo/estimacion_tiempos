from django.urls import path

from .views import RegistrarCliente

app_name = 'usuarios'

urlpatterns = [
    path('registrar_cliente/', RegistrarCliente.as_view(), name='registrar_cliente'),
]
from django.urls import path

from .views import (RegistrarCliente,
                    ListadoCliente,
                    RegistrarProgramador,
                    ListadoProgramador)

app_name = 'usuarios'

urlpatterns = [
    path('registrar-cliente/', RegistrarCliente.as_view(), name='registrar_cliente'),
    path('listado-clientes/', ListadoCliente.as_view(), name='listado_clientes'),

    path('registrar-programador/', RegistrarProgramador.as_view(), name='registrar_programador'),
    path('listado-programadores/', ListadoProgramador.as_view(), name='listado_programadores'),
]
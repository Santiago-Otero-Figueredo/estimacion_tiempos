from django.urls import path

from .views import (RegistrarCliente,
                    ListadoCliente,
                    RegistrarProgramador,
                    ListadoProgramador,
                    ListadoAdministradores,
                    RegistrarAdministrador,
                    InicioSesion,
                    CerrarSesion)

app_name = 'usuarios'

urlpatterns = [
    path('iniciar-sesion/', view=InicioSesion.as_view(), name='iniciar_sesion'),
    path('cerrar-sesion/', view=CerrarSesion.as_view(), name='cerrar_sesion'),

    path('registrar-cliente/', RegistrarCliente.as_view(), name='registrar_cliente'),
    path('listado-clientes/', ListadoCliente.as_view(), name='listado_clientes'),

    path('registrar-programador/', RegistrarProgramador.as_view(), name='registrar_programador'),
    path('listado-programadores/', ListadoProgramador.as_view(), name='listado_programadores'),

    path('registrar-administradores/', RegistrarAdministrador.as_view(), name='registrar_administrador'),
    path('listado-administradores/', ListadoAdministradores.as_view(), name='listado_administradores'),
]


from django.urls import path

from .views import (RegistrarEmpresa,
                    ListadoEmpresas,
                    RegistrarTrabajador,
                    ListadoTrabajadores,
                    ListadoAdministradores,
                    RegistrarAdministrador,
                    RegistrarCargo,
                    ListadoCargos,
                    InicioSesion,
                    CerrarSesion)

app_name = 'usuarios'

urlpatterns = [
    path('iniciar-sesion/', view=InicioSesion.as_view(), name='iniciar_sesion'),
    path('cerrar-sesion/', view=CerrarSesion.as_view(), name='cerrar_sesion'),

    path('registrar-empresa/', RegistrarEmpresa.as_view(), name='registrar_empresa'),
    path('listado-empresas/', ListadoEmpresas.as_view(), name='listado_empresas'),

    path('registrar-trabajador/', RegistrarTrabajador.as_view(), name='registrar_trabajador'),
    path('listado-trabajador/', ListadoTrabajadores.as_view(), name='listado_trabajadores'),

    path('registrar-administradores/', RegistrarAdministrador.as_view(), name='registrar_administrador'),
    path('listado-administradores/', ListadoAdministradores.as_view(), name='listado_administradores'),

    path('registrar-cargo/', RegistrarCargo.as_view(), name='registrar_cargo'),
    path('listado-cargos/', ListadoCargos.as_view(), name='listado_cargos'),
]


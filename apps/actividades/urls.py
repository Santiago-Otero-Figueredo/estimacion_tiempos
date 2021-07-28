from django.urls import path

from .views import (
                    RegistrarActividad,
                    ListadoActividad,
                    RegistrarTipoActividad,
                    ListadoTipoActividad,
                    ImportarActividadesJIRA,
                    ObtenerActividadesComunes,
                    ModificarActividad,
                    ModificarTipoActividad,
                    AsociarActividadesSinTipos,
                    )


app_name = 'actividades'

urlpatterns = [
    path('registrar-actividad/', RegistrarActividad.as_view(), name='registrar_actividad'),
    path('modificar-actividad/<int:pk>', ModificarActividad.as_view(), name='modificar_actividad'),
    path('listado-actividades/', ListadoActividad.as_view(), name='listado_actividades'),
    path('asignar-tipos-actividades/', AsociarActividadesSinTipos.as_view(), name='asignar_tipos_actividades'),

    path('registrar-tipo-actividad/', RegistrarTipoActividad.as_view(), name='registrar_tipo_actividad'),
    path('modificar-tipo-actividad/<int:pk>', ModificarTipoActividad.as_view(), name='modificar_tipo_actividad'),
    path('listado-tipos-actividades/', ListadoTipoActividad.as_view(), name='listado_tipos_actividades'),

    path('obtener-actividades-comunes/', ObtenerActividadesComunes.as_view(), name='api_obtener_actividades_comunes'),

    path('importar-actividades-jira/', ImportarActividadesJIRA.as_view(), name='importar_actividades_jira'),
]
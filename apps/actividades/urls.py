from django.urls import path

from .views import (
                    RegistrarActividad,
                    ListadoActividad,
                    RegistrarTipoActividad,
                    ListadoTipoActividad,
                    ObtenerActividadesComunes,
                    )


app_name = 'actividades'

urlpatterns = [
    path('registrar-actividad/', RegistrarActividad.as_view(), name='registrar_actividad'),
    path('listado-actividades/', ListadoActividad.as_view(), name='listado_actividades'),

    path('registrar-tipo-actividad/', RegistrarTipoActividad.as_view(), name='registrar_tipo_actividad'),
    path('listado-tipos-actividades/', ListadoTipoActividad.as_view(), name='listado_tipos_actividades'),

    path('obtener-actividades-comunes/', ObtenerActividadesComunes.as_view(), name='api_obtener_actividades_comunes'),

]
from apps.estimaciones.views.tipos_actividad import ListadoTipoActividad, RegistrarTipoActividad
from django.urls import path

from .views import (RegistrarProyecto,
                    ListadoProyecto,
                    RegistrarProyectoEmpleado,
                    ListadoProyectosEmpleados,
                    RegistrarActividad,
                    ListadoActividad,
                    RegistrarTipoActividad,
                    ListadoTipoActividad,
                    ObtenerActividadesComunes,
                    ObtenerEstimacionesActividades)


app_name = 'estimaciones'

urlpatterns = [
    path('registrar-proyecto/', RegistrarProyecto.as_view(), name='registrar_proyecto'),
    path('listado-proyectos/', ListadoProyecto.as_view(), name='listado_proyectos'),

    path('registrar-proyecto-empleado/', RegistrarProyectoEmpleado.as_view(), name='registrar_proyecto_empleado'),
    path('listado-proyectos-empleado/', ListadoProyectosEmpleados.as_view(), name='listado_proyecto_empleados'),

    path('registrar-actividad/', RegistrarActividad.as_view(), name='registrar_actividad'),
    path('listado-actividades/', ListadoActividad.as_view(), name='listado_actividades'),

    path('registrar-tipo-actividad/', RegistrarTipoActividad.as_view(), name='registrar_tipo_actividad'),
    path('listado-tipos-actividades/', ListadoTipoActividad.as_view(), name='listado_tipos_actividades'),

    path('obtener-estimaciones-actividades/', ObtenerEstimacionesActividades.as_view(), name='obtener_estimaciones_actividades'),
    
    path('obtener-actividades-comunes/', ObtenerActividadesComunes.as_view(), name='api_obtener_actividades_comunes'),

]
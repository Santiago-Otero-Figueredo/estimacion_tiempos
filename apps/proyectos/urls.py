from django.urls import path

from .views import (RegistrarProyecto,
                    ListadoProyecto,
                    ModificarProyecto,
                    RegistrarProyectoEmpleado,
                    ListadoProyectosEmpleados,
                    ModificarProyectoEmpleado)


app_name = 'proyectos'

urlpatterns = [
    path('registrar-proyecto/', RegistrarProyecto.as_view(), name='registrar_proyecto'),
    path('modificar-proyecto/<int:pk>', ModificarProyecto.as_view(), name='modificar_proyecto'),
    path('listado-proyectos/', ListadoProyecto.as_view(), name='listado_proyectos'),

    path('registrar-proyecto-empleado/', RegistrarProyectoEmpleado.as_view(), name='registrar_proyecto_empleado'),
    path('modificar-proyecto-empleado/<int:pk>', ModificarProyectoEmpleado.as_view(), name='modificar_proyecto_empleado'),    
    path('listado-proyectos-empleado/', ListadoProyectosEmpleados.as_view(), name='listado_proyecto_empleados'),
]
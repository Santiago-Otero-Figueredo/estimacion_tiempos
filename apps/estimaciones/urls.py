from django.urls import path

from .views import (RegistrarProyecto,
                    ListadoProyecto)


app_name = 'estimaciones'

urlpatterns = [
    path('registrar-proyecto/', RegistrarProyecto.as_view(), name='registrar_proyecto'),
    path('listado-proyectos/', ListadoProyecto.as_view(), name='listado_proyectos'),
]
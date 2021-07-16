
from django.urls import path

from .views import ObtenerEstimacionesActividades


app_name = 'estimaciones'

urlpatterns = [ 
    path('obtener-estimaciones-actividades/', ObtenerEstimacionesActividades.as_view(), name='obtener_estimaciones_actividades'),
]
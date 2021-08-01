from django.urls import path

from .views import (
    TableroParticipacion,
    TableroDistribucion,
    TableroTiempos
)

app_name = 'dashboard'

urlpatterns = [
    path("tablero-participacion", TableroParticipacion.as_view(), name="tablero_participacion"),
    path("tablero-distribucion", TableroDistribucion.as_view(), name="tablero_distribucion"),
    path("tablero-tiempos", TableroTiempos.as_view(), name="tablero_tiempos"),

    
]
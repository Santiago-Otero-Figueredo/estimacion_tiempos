from django.urls import path

from apps.prueba.views import TablerosHoras

app_name = 'pruebas'

urlpatterns = [
    path('prueba/', view=TablerosHoras.as_view(), name='prueba'),
]
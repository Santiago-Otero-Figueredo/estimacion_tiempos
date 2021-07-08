from django.db import models

from apps.utils.models import EstimacionModel


class TipoActividad(EstimacionModel):
    nombre = models.CharField('Nombre tipo actividad', max_length=100, unique=True)

    def __str__(self):

        return self.nombre


    @staticmethod
    def buscar_por_nombre(nombre:str) -> 'TipoActividad':
        try:
            return TipoActividad.objects.get(nombre=nombre)
        except TipoActividad.DoesNotExist:
            return None
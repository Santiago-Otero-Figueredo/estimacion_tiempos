from django.db import models

from apps.utils.models import EstimacionModel


class TipoActividad(EstimacionModel):
    nombre = models.CharField('Nombre tipo actividad', max_length=100, unique=True)
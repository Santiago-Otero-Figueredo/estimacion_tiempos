from django.db import models

from apps.utils.models import TiposModel


class TipoActividad(TiposModel):
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)


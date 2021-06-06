from django.db import models


from apps.utils.models import EstimacionModel

from apps.estimaciones.models.actividades import Actividad

class Estado(EstimacionModel):
    actividad = models.ForeignKey(
        Actividad, 
        related_name="estados_actividad", 
        verbose_name="Estados de la actividad", 
        on_delete=models.PROTECT
    )
    nombre = models.CharField('Nombre estado', max_length=25)
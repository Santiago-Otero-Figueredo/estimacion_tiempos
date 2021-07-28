from django.db import models


from apps.utils.models import EstimacionModel

class CaminoActividad(EstimacionModel):
    actividad = models.ForeignKey(
        'Actividad',
        related_name='actividad_caminos',
        verbose_name="Actividad",
        on_delete=models.PROTECT
    )
    tipo_actividad = models.ForeignKey(
        'TipoActividad',
        related_name='tipo_actividad_caminos',
        verbose_name="Tipo actividad",
        on_delete=models.PROTECT
    )
    

    def __str__(self) -> str:
        return "{}-{}".format(self.tipo_actividad, self.actividad)
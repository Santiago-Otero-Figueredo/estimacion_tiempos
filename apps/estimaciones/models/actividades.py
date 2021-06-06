from django.db import models

from apps.utils.models import EstimacionModel

from apps.estimaciones.models.tipos_actividades import TipoActividad

class Actividad(EstimacionModel):
    tipo_Actividad = models.ForeignKey(TipoActividad, on_delete=models.PROTECT, verbose_name="Tipo de actividad asociado")
    funcionalidad = models.CharField('Funcionalidad especifica del proyecto', max_length=255)
    fecha_inicio = models.DateTimeField(
        'Iniciado a',
        auto_now_add=True,
        help_text='Fecha y hora en la que se inicio el proyecto'
    )
    fecha_finalizacion = models.DateTimeField(
        'Finalizado a',
        auto_now=True,
        help_text='Fecha y hora de finalización del proyecto'
    )
    tiempo_estimado = models.PositiveIntegerField('Tiempo estimado (segundos)')
    tiempo_real = models.PositiveIntegerField('Tiempo real (segundos)')
    
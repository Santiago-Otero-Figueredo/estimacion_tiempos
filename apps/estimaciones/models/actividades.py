from django.db import models
from django.db.models import Avg, Q

from apps.utils.models import EstimacionModel

from apps.estimaciones.models.tipos_actividades import TipoActividad
from apps.estimaciones.models.proyecto_programador import ProyectoProgramador

class Actividad(EstimacionModel):
    tipo_actividad = models.ForeignKey(TipoActividad, on_delete=models.PROTECT, related_name="actividad_del_tipo",verbose_name="Tipo de actividad asociado")
    proyecto_programador = models.ForeignKey(ProyectoProgramador, on_delete=models.PROTECT, related_name="actividad_proyecto_programador", verbose_name="Proyecto y programador asociados")
    funcionalidad = models.CharField('Funcionalidad especifica del proyecto', max_length=255)
    fecha_inicio = models.DateTimeField(
        'Iniciado a',        
        help_text='Fecha y hora en la que se inicio el proyecto',
        blank=True, null=True
    )
    fecha_finalizacion = models.DateTimeField(
        'Finalizado a',        
        help_text='Fecha y hora de finalización del proyecto',
        blank=True, null=True
    )
    tiempo_estimado = models.PositiveIntegerField('Tiempo estimado (minutos)')
    tiempo_real = models.PositiveIntegerField('Tiempo real (minutos)')

    @staticmethod
    def obtener_actividades_por_nombre(nombre:str) -> 'Queryset<Actividad>':
        """ Retorna las actividades que contengan el nombre recibido en la funcionalidad """

        return Actividad.objects.filter(
            Q(funcionalidad__icontains=nombre) |
            Q(tipo_actividad__nombre__icontains=nombre)
        ).values(
            "tipo_actividad__nombre",
        ).annotate(tiempo_promedio=Avg('tiempo_real')
        ).order_by('-tiempo_promedio')
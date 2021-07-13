from django.db import models
from django.db.models import Avg, Q

from apps.utils.models import EstimacionModel

from apps.estimaciones.models.tipos_actividades import TipoActividad
from apps.estimaciones.models.proyectos_empleados import ProyectoEmpleado


class Actividad(EstimacionModel):
    tipo_actividad = models.ForeignKey(
        TipoActividad,
        on_delete=models.SET_DEFAULT,
        related_name="actividades_del_tipo_actividad",
        verbose_name="Tipo de actividad asociado",
        default=1
    )
    proyecto_empleado = models.ForeignKey(
        ProyectoEmpleado,
        on_delete=models.SET_NULL,
        related_name="actividad_proyecto_empleado",
        verbose_name="Proyecto y empleado asociados",
        null=True
    )
    identificador = models.CharField(max_length=20, verbose_name="Identificador único según el tipo de insumo", null=True, blank=True)
    funcionalidad = models.CharField('Funcionalidad especifica del proyecto', max_length=255)
    fecha_inicio = models.DateTimeField(
        'Iniciado a',
        help_text='Fecha y hora en la que se inicio la actividad',
        blank=True, null=True
    )
    fecha_finalizacion = models.DateTimeField(
        'Finalizado a',
        help_text='Fecha y hora de finalización de la actividad',
        blank=True, null=True
    )
    tiempo_estimado = models.PositiveIntegerField('Tiempo estimado (minutos)')
    tiempo_real = models.PositiveIntegerField('Tiempo real (minutos)')


    """@staticmethod
    def obtener_actividades_por_nombre(nombre:str) -> 'Queryset<Actividad>':

        return Actividad.objects.filter(
            Q(funcionalidad__icontains=nombre) |
            Q(tipo_actividad__nombre__icontains=nombre)
        ).values(
            "tipo_actividad__nombre",
        ).annotate(tiempo_promedio=Avg('tiempo_real')
        ).order_by('-tiempo_promedio')"""
    
    @staticmethod
    def obtener_actividades_por_nombre(nombre:str) -> 'Queryset<Actividad>':
        """ Retorna las actividades que contengan el nombre recibido en la funcionalidad """

        return Actividad.objects.filter(
            Q(funcionalidad__icontains=nombre) |
            Q(tipo_actividad__nombre__icontains=nombre)
        ).values(
            'identificador', 'tipo_actividad__nombre', 'fecha_inicio',
            'fecha_finalizacion', 'tiempo_estimado', 'tiempo_real'
        )
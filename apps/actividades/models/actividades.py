from django.db import models
from django.db.models import Q, Count
from django.contrib.postgres.fields import ArrayField

from ..models.tipos_actividades import TipoActividad

from apps.proyectos.models.proyectos_empleados import ProyectoEmpleado
from apps.utils.models import EstimacionModel
from .caminos_actividades import CaminoActividad


class Actividad(EstimacionModel):
    tipos_actividades = models.ManyToManyField(
        TipoActividad,
        related_name="actividades_del_tipo_actividad",
        verbose_name="Tipo de actividad asociado",
        through=CaminoActividad
    )
    slug_tipos = models.CharField(max_length=255, verbose_name="Descripción de los tipos asociados a la actividad", null=True, blank=True)
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

    def __str__(self) -> str:
        return "{}".format(self.identificador)

    @staticmethod
    def obtener_actividades_por_nombre(nombre:str) -> 'Queryset<Actividad>':
        """ Retorna las actividades que contengan el nombre recibido en la funcionalidad """

        return Actividad.objects.exclude(funcionalidad__exact="").filter(
            Q(funcionalidad__icontains=nombre) |
            #Q(funcionalidad__trigram_similar=nombre) |
            Q(slug_tipos__icontains=nombre) |
            Q(tipos_actividades__nombre__icontains=nombre)

        ).values(
            'tipos_actividades__nombre', 'tiempo_estimado', 'tiempo_real', 'slug_tipos'
        )


    @staticmethod
    def obtener_por_identificador_jira(identificador:str) -> 'Actividad':
        
        try:
            return Actividad.objects.get(identificador=identificador)
        except Actividad.DoesNotExist:
            return Actividad.objects.none()

    @staticmethod
    def obtener_actividades_sin_tipos() -> 'Actividad':
        return Actividad.objects.filter(tipos_actividades__isnull=True)

    @staticmethod
    def obtener_actividades_similares(nombre_actividad:str) -> 'Actividad':

        tipo_similares = TipoActividad.objects.none()
        if not nombre_actividad is None and nombre_actividad != '':
            actividades_similares = Actividad.objects.exclude(slug_tipos__isnull=True).exclude(slug_tipos__exact='').exclude(funcionalidad="").filter(
                Q(funcionalidad__icontains=str(nombre_actividad)) |
                Q(funcionalidad__trigram_similar=str(nombre_actividad)) |
                Q(slug_tipos__icontains=str(nombre_actividad)) |
                Q(tipos_actividades__nombre__icontains=str(nombre_actividad))
            ).values(
                'slug_tipos'
            ).annotate(total=Count('slug_tipos')).order_by('-total').values('pk', 'slug_tipos', 'total').first()
            
            if actividades_similares:
                actividad_mayor_similitud = Actividad.objects.get(pk=actividades_similares['pk'])
                tipo_similares = actividad_mayor_similitud.tipos_actividades.all()

        return tipo_similares

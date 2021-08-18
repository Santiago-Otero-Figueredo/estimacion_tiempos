from django.db import models

from apps.utils.models import EstimacionModel

from apps.usuarios.models.empleados import Empleado
from ..models.proyectos import Proyecto

class ProyectoEmpleado(EstimacionModel):
    empleado = models.ForeignKey(
        Empleado,
        related_name='proyectos_empleado_empleado',
        verbose_name="Empleado*",
        on_delete=models.PROTECT
    )
    proyecto = models.ForeignKey(
        Proyecto,
        related_name='proyectos_empleado_proyecto',
        verbose_name="Proyecto*",
        on_delete=models.PROTECT
    )
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

    def __str__(self) -> str:
        return "{}-{}".format(self.proyecto, self.empleado)

    @staticmethod
    def crear_y_obtener(empleado:'Empleado', proyecto:'Proyecto') -> 'TipoActividad':

        if ProyectoEmpleado.existe(empleado, proyecto):
            return ProyectoEmpleado.buscar_por_empleado_y_proyecto(empleado, proyecto)
        else:
            ProyectoEmpleado.objects.create(empleado=empleado, proyecto=proyecto)
       

    @staticmethod
    def existe(empleado:'Empleado', proyecto:'Proyecto') -> bool:
        try:
            ProyectoEmpleado.objects.get(empleado=empleado, proyecto=proyecto)
            return True
        except ProyectoEmpleado.DoesNotExist:
            return False

    @staticmethod
    def buscar_por_empleado_y_proyecto(empleado:'Empleado', proyecto:'Proyecto') -> "ProyectoEmpleado":
        try:
            return ProyectoEmpleado.objects.get(empleado=empleado, proyecto=proyecto)
        except ProyectoEmpleado.DoesNotExist:
            return None
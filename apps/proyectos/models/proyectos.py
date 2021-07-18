from django.db import models

from apps.utils.models import EstimacionModel

from apps.usuarios.models.empresas import Empresa
from apps.usuarios.models.empleados import Empleado

class Proyecto(EstimacionModel):
    empresa = models.ForeignKey(
        Empresa,
        related_name='proyectos_empresa', 
        verbose_name="Empresas asociadas al proyecto",
        on_delete=models.PROTECT
    )
    empleados = models.ManyToManyField(
        Empleado,
        through='ProyectoEmpleado',
        related_name="proyecto_empleado",
        blank=True,
        verbose_name="Empleados asociados al proyecto"
    )
    identificador_jira = models.CharField(max_length=80, unique=True, verbose_name="Identificador del proyecto JIRA")
    nombre = models.CharField(max_length=80, unique=True, verbose_name="Nombre del proyecto")
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
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

    def __str__(self):
        """Return username."""
        return self.nombre

    
    @staticmethod
    def buscar_por_nombre(nombre:str) -> 'Proyecto':
        try:
            return Proyecto.objects.get(nombre=nombre)
        except Proyecto.DoesNotExist:
            return None
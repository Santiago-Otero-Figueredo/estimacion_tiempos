from django.db import models

from apps.utils.models import EstimacionModel

from apps.usuarios.models.clientes import Cliente
from apps.usuarios.models.programadores import Programador

class Proyecto(EstimacionModel):
    cliente = models.ForeignKey(
        Cliente,
        related_name='proyectos_cliente', 
        verbose_name="Proyectos asociados a un cliente",
        on_delete=models.PROTECT
    )
    nombre = models.CharField(max_length=80, unique=True)
    programadores = models.ManyToManyField(
        Programador,
        through='ProyectoProgramador',
        related_name="proyecto_programador",
        blank=True,
        verbose_name="programadores asociados al proyecto"
    )
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
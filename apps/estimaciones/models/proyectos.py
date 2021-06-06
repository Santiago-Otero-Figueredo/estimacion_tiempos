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
    programadores = models.ManyToManyField(
        Programador, 
        through='ProyectoProgramador', 
        related_name="proyecto_programador", 
        blank=True, 
        verbose_name="programadores asociados al proyecto"
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
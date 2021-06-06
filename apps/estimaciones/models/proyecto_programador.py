from django.db import models

from apps.utils.models import EstimacionModel

from apps.usuarios.models.programadores import Programador
from apps.estimaciones.models.proyectos import Proyecto

class ProyectoProgramador(EstimacionModel):
    programador = models.ForeignKey(
        Programador, 
        related_name='proyectos_programador_programador', 
        verbose_name="Programador",
        on_delete=models.PROTECT
    )
    proyecto = models.ForeignKey(
        Proyecto, 
        related_name='proyectos_programador_proyecto', 
        verbose_name="Proyecto",
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
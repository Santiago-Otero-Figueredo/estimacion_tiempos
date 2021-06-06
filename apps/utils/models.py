"""Django models utilities."""

# Django
from django.db import models


class EstimacionModel(models.Model):   

    creado = models.DateTimeField(
        'creado a',
        auto_now_add=True,
        help_text='Fecha y hora en la que se ha creado el objeto'
    )
    modificado = models.DateTimeField(
        'modificado a',
        auto_now=True,
        help_text='Fecha y hora de la ultima modificación'
    )
    esta_activo = models.BooleanField(default=True)
    
    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'creado'
        ordering = ['-creado', '-modificado']
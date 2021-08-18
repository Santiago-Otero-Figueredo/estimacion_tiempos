# Django
from django.db import models
from django.core.validators import RegexValidator

# Utilities
from apps.utils.models import EstimacionModel
from ..models import Proyecto


class ContactoProyecto(EstimacionModel):
    proyecto = models.ForeignKey(
        Proyecto,
        related_name='contactos_empresa_proyecto',
        verbose_name="Proyecto*",
        on_delete=models.PROTECT
    )
    nombres = models.CharField(max_length=75, verbose_name="Nombres del contacto*")
    apellidos = models.CharField(max_length=75, verbose_name="Apellidos del contacto*")
    correo_electronico = models.EmailField('Correo electrónico*')
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{7,10}$',
        message="El numero de teléfono debe tener entre 7 y 10 digitos:"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Teléfono celular')
    cargo = models.CharField(max_length=100, verbose_name="Cargo del contacto en la empresa a la que pertenece", default='')

    def __str__(self):
        """Return username."""
        return self.username

    @classmethod
    def buscar_por_id(cls, id_elemento:int) -> 'Usuario':
        try:
            return cls.objects.get(pk=id_elemento)
        except cls.DoesNotExist:
            return cls.objects.none()


    @classmethod
    def existe_por_id(cls, id_elemento:int) -> bool:
        return cls.objects.filter(pk=id_elemento).exists()


    @classmethod
    def buscar_por_correo_electronico(cls, correo_electronico:str) -> 'Usuario':
        try:
            return cls.objects.get(correo_electronico=correo_electronico)
        except cls.DoesNotExist:
            return cls.objects.none()

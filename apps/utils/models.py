"""Django models utilities."""

# Django
from django.db import models
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

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

    def save(self, *args, **kwargs):
        self.modificado = timezone.now()
        return super().save(*args, **kwargs)


    @classmethod
    def obtener_activos(cls):
        return cls.objects.filter(esta_activo=True)

    @classmethod
    def obtener_todos(cls):
        return cls.objects.all()

    @classmethod
    def buscar_por_id(cls, id_elemento:int) -> 'EstimacionModel':
        try:
            return cls.objects.get(pk=id_elemento)
        except ObjectDoesNotExist:
            return cls.objects.none()

    @classmethod
    def existe_por_id(cls, id_elemento:int) -> bool:
        return cls.objects.filter(pk=id_elemento).exists()


    def desactivar_elemento(self) -> None:
        self.esta_activo = False
        self.save()


    def activar_elemento(self) -> None:
        self.esta_activo = True
        self.save()


class TiposModel(EstimacionModel):
    identificador = models.PositiveIntegerField(
        verbose_name="Identificador único",
        help_text="""Permite mantener constante el identificador para evitar inconvenientes 
                    de los posibles cambios de id que puedan generar las migraciones""", 
        default=0,
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre del tipo", unique=True)

    class Meta:
        """Meta option."""
        abstract = True
        unique_together = (('identificador', 'nombre'),)

    
    def __str__(self):
        return self.nombre

    @classmethod
    def buscar_por_identificador(cls, identificador:int) -> 'TiposModel':
        try:
            return cls.objects.get(identificador=identificador)
        except ObjectDoesNotExist:
            return cls.objects.none()


    @classmethod
    def existe_por_identificador(cls, identificador:int) -> bool:
        return cls.objects.filter(identificador=identificador).exists()


    @classmethod
    def buscar_por_nombre(cls, nombre:str) -> 'TiposModel':
        try:
            return cls.objects.get(nombre=nombre)
        except ObjectDoesNotExist:
            return cls.objects.none()

    
    @classmethod
    def buscar_por_lista_ids(cls, lista_ids:'list<int>') -> 'TiposModel':
        return cls.objects.filter(pk__in=lista_ids)


    @classmethod
    def existe_por_nombre(cls, nombre:str) -> bool:
        return cls.objects.filter(nombre=nombre).exists()

    @classmethod
    def obtener_identificador_mayor(cls) -> bool:
        elemento = cls.objects.order_by('identificador').first()
        if elemento:
            return elemento.identificador
        return 0





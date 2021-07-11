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

    @classmethod
    def obtener_activos(cls):
        return cls.objects.filter(esta_activo=True)

    @classmethod
    def obtener_todos(cls):
        return cls.objects.all()


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
        except cls.DoesNotExist:
            return cls.objects.none()


    @classmethod
    def existe_por_identificador(cls, identificador:int) -> bool:
        return cls.objects.filter(identificador=identificador).exists()


    @classmethod
    def buscar_por_nombre(cls, nombre:str) -> 'TiposModel':
        try:
            return cls.objects.get(nombre=nombre)
        except cls.DoesNotExist:
            return cls.objects.none()


    @classmethod
    def existe_por_nombre(cls, nombre:str) -> bool:
        return cls.objects.filter(nombre=nombre).exists()





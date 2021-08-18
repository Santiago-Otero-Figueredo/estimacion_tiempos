from django.db import models

from apps.utils.models import TiposModel



class TipoActividad(TiposModel):
    estructura = models.ForeignKey("Estructura", verbose_name="Estructura asociada*", related_name="tipos_actividades_estructura", on_delete=models.PROTECT)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)

    class Meta:
        ordering = ['estructura__pk']

    @staticmethod
    def existe_tupla_de_tipos(tipo_padre:'TipoActividad', tipo_hijo:'TipoActividad'):
        return (tipo_hijo.tipo_superior == tipo_padre)

    def asociar_tupla_padre(self, tipo_padre:'TipoActividad'):
        self.tipo_superior = tipo_padre
        self.save()





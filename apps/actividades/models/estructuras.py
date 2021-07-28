from django.db import models

from apps.utils.models import TiposModel


class Estructura(TiposModel):
    pass

    @staticmethod
    def obtener_estructura_lugar():
        return Estructura.objects.get(identificador=1)

    @staticmethod
    def obtener_estructura_accion():
        return Estructura.objects.get(identificador=2)

    @staticmethod
    def obtener_estructura_tarea():
        return Estructura.objects.get(identificador=3)

    @staticmethod
    def obtener_estructura_adicional():
        return Estructura.objects.get(identificador=4)

    @staticmethod
    def obtener_actividades_lugar():
        return Estructura.obtener_estructura_lugar().tipos_actividades_estructura.all().order_by('nombre')

    @staticmethod
    def obtener_actividades_accion():
        return Estructura.obtener_estructura_accion().tipos_actividades_estructura.all().order_by('nombre')

    @staticmethod
    def obtener_actividades_tarea():
        return Estructura.obtener_estructura_tarea().tipos_actividades_estructura.all().order_by('nombre')

    @staticmethod
    def obtener_actividades_adicional():
        return Estructura.obtener_estructura_adicional().tipos_actividades_estructura.all().order_by('nombre')



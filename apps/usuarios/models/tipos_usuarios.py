from django.db import models

from apps.utils.models import TiposModel

class TipoUsuario(TiposModel):
    pass

    @staticmethod
    def obtener_tipo_trabajador():
        return TipoUsuario.buscar_por_identificador(1)

    @staticmethod
    def obtener_tipo_empresa():
        return TipoUsuario.buscar_por_identificador(2)

    @staticmethod
    def obtener_tipo_administrador():
        return TipoUsuario.buscar_por_identificador(3)
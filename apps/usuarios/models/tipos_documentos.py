from django.db import models

from apps.utils.models import TiposModel

class TipoDocumento(TiposModel):
    pass

    @staticmethod
    def obtener_tipo_ninguno():
        return TipoDocumento.buscar_por_identificador(1)

    @staticmethod
    def obtener_tipo_nit():
        return TipoDocumento.buscar_por_identificador(2)

    @staticmethod
    def obtener_tipo_cedula():
        return TipoDocumento.buscar_por_identificador(3)

from django.core.management.base import BaseCommand

from apps.usuarios.models import TipoDocumento

import pandas as pd

class Command(BaseCommand):
    help = 'Carga los tipos de documentos'

    def handle(self, *args, **kwargs):
        tipos = pd.read_csv("_data/cargar_inicio_proyecto/1_tipos/1_tipos_documentos.csv")
        for _, documento in tipos.iterrows():
            nombre = documento['nombre']
            identificador = documento['identificador']
            if not TipoDocumento.existe_por_identificador(identificador):
                TipoDocumento.objects.create(
                    nombre=nombre.capitalize(),
                    identificador=identificador,
                )
                print(("--> El tipo de documento {} fue creado con el numero identificador ({}) ".format(nombre, identificador)))
            else:
                print("--> El tipo de documento con el identificador ({}) no fue creado porque ya existe en la base de datos".format(identificador))
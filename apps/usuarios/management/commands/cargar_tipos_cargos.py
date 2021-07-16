from django.core.management.base import BaseCommand

from apps.usuarios.models import TipoCargo

import pandas as pd

class Command(BaseCommand):
    help = 'Carga los tipos de usuarios'

    def handle(self, *args, **kwargs):
        cargos = pd.read_csv("_data/cargar_inicio_proyecto/1_tipos/3_tipos_cargos.csv")
        for _, usuario in cargos.iterrows():
            nombre = usuario['nombre']
            identificador = usuario['identificador']
            if not TipoCargo.existe_por_identificador(identificador):
                TipoCargo.objects.create(
                    nombre=nombre.capitalize(),
                    identificador=identificador,
                )
                print(("--> El tipo de cargo {} fue creado con el numero identificador ({}) ".format(nombre, identificador)))
            else:
                print("--> El tipo de cargo con el identificador ({}) no fue creado porque ya existe en la base de datos".format(identificador))
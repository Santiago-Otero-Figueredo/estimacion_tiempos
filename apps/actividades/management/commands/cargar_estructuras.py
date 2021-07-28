from django.core.management.base import BaseCommand

from apps.actividades.models import Estructura

import pandas as pd

class Command(BaseCommand):
    help = 'Carga los tipos de estructuras'

    def handle(self, *args, **kwargs):
        estructuras = pd.read_csv("_data/cargar_inicio_proyecto/1_tipos/4_estructuras.csv")
        for _, estructura in estructuras.iterrows():
            nombre = estructura['nombre']
            identificador = estructura['identificador']
            if not Estructura.existe_por_identificador(identificador):
                Estructura.objects.create(
                    nombre=nombre.capitalize(),
                    identificador=identificador,
                )
                print(("--> La estructura {} fue creado con el numero identificador ({}) ".format(nombre, identificador)))
            else:
                print("--> La estructura con el identificador ({}) no fue creado porque ya existe en la base de datos".format(identificador))
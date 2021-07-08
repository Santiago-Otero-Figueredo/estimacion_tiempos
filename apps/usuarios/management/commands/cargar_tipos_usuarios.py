from django.core.management.base import BaseCommand

from apps.usuarios.models import TipoUsuario

import pandas as pd

class Command(BaseCommand):
    help = 'Carga los tipos de usuarios'

    def handle(self, *args, **kwargs):
        tipos = pd.read_csv("_data/cargar_inicio_proyecto/1_tipos/tipos_usuarios.csv")
        for _, ciudad in tipos.iterrows():
            nombre = ciudad['nombre']
            identificador = ciudad['identificador']
            if not TipoUsuario.existe_por_identificador(identificador):
                TipoUsuario.objects.create(
                    nombre=nombre.capitalize(),
                    identificador=identificador,
                )
                print(("--> El tipo de usuario {} fue creado con el numero identificador ({}) ".format(nombre, identificador)))
            else:
                print("--> El tipo de usuario con el identificador ({}) no fue creado porque ya existe en la base de datos".format(identificador))
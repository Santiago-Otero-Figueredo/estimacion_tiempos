from django.core.management.base import BaseCommand

from apps.usuarios.models import (Usuario,
                                  Administrador,
                                  Empresa,
                                  Empleado,
                                  Trabajador
                                )

import pandas as pd

class Command(BaseCommand):
    help = 'Carga los usuarios iniciales'

    def handle(self, *args, **kwargs):
        usuarios = pd.read_csv("_data/cargar_inicio_proyecto/2_usuarios/1_usuarios.csv")
        for _, documento in usuarios.iterrows():

            pk = documento['id']
            password = documento['password']
            last_login = documento['last_login']
            is_superuser = documento['is_superuser']
            username = documento['username']
            first_name = documento['first_name']
            last_name = documento['last_name']
            is_staff = documento['is_staff']
            is_active = documento['is_active']
            date_joined = documento['date_joined']
            creado = documento['creado']
            modificado = documento['modificado']
            email = documento['email']
            phone_number = documento['phone_number']
            is_verified = documento['is_verified']
            esta_activo = documento['esta_activo']
            tipo_documento_id = documento['tipo_documento_id']
            tipo_usuario_id = documento['tipo_usuario_id']

            if not Usuario.existe_por_id(pk):
                Usuario.objects.create(
                    pk=pk,
                    password=password,
                    last_login=last_login,
                    is_superuser=is_superuser,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=is_staff,
                    is_active=is_active,
                    date_joined=date_joined,
                    creado=creado,
                    modificado=modificado,
                    email=email,
                    phone_number=phone_number,
                    is_verified=is_verified,
                    esta_activo=esta_activo,
                    tipo_documento_id=tipo_documento_id,
                    tipo_usuario_id=tipo_usuario_id
                )
                print("--> El usuario con correo {} fue creado exitosamente".format(email))
            else:
                print("--> El usuario con correo ({}) no fue creado porque ya existe en la base de datos".format(email))

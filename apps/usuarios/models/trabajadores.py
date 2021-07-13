from django.db import models

from apps.usuarios.models.empleados import Empleado
from apps.usuarios.models.tipos_usuarios import TipoUsuario

class Trabajador(Empleado):
    pass

    def save(self, *args, **kwargs):
        self.tipo_usuario = TipoUsuario.buscar_por_identificador(1)
        return super().save(*args, **kwargs)
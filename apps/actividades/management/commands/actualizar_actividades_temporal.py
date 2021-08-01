
from django.core.management.base import BaseCommand


from ...models.actividades import Actividad
from ...utils import crear_slug_tipos_actividad

from apps.proyectos.models.proyectos import Proyecto
from apps.proyectos.models.proyectos_empleados import ProyectoEmpleado

from apps.usuarios.models.empleados import Empleado
from apps.utils.clases.jira.ConexionJira import Jira

import re

class Command(BaseCommand):
    help = 'Carga los datos iniciales de las historias de usuario desde un archivo Excel'

    def handle(self, *args, **kwargs):

        actividades = Actividad.obtener_todos()

        for actividad in actividades:
            tipos = actividad.tipos_actividades.all()
            if len(tipos) >= 3:
                
                tipo_1 = tipos[0]
                tipo_2 = tipos[1]
                tipo_3 = tipos[2]
                tipo_adicional = None

                if len(tipos) == 4:
                    tipo_adicional = tipos[3].nombre

                slug_tipos = crear_slug_tipos_actividad(tipo_1.nombre, tipo_2.nombre, tipo_3.nombre, tipo_adicional)
                actividad.slug_tipos = slug_tipos
                actividad.save()
                print(actividad, "Actualizada", slug_tipos)

       


from django.core.management.base import BaseCommand

from apps.prueba.utils import GestorLectorExcel

from ...models.actividades import Actividad
from ...models.tipos_actividades import TipoActividad
from ...models.caminos_actividades import CaminoActividad

from apps.proyectos.models.proyectos import Proyecto
from apps.proyectos.models.proyectos_empleados import ProyectoEmpleado

from apps.usuarios.models.empleados import Empleado
from apps.utils.clases.jira.ConexionJira import Jira

import re

class Command(BaseCommand):
    help = 'Carga los datos iniciales de las historias de usuario desde un archivo Excel'

    def handle(self, *args, **kwargs):

        jira = Jira()
        proyecto_buscar = 'KT'
        historias_usuario = jira.consultar_historias_usuarios(proyecto_buscar)
        for histroia_usuario in historias_usuario:
            try:
                proyecto_registrado = Proyecto.buscar_por_identificador_jira(proyecto_buscar)
                empleado = Empleado.buscar_por_nombre_y_apellido(histroia_usuario['nombre_usuario_asignado'].strip()).first()
                actividad = Actividad.obtener_por_identificador_jira(histroia_usuario['key'])
                if empleado and actividad.count() == 0:
                    proyecto_empleado = ProyectoEmpleado.crear_y_obtener(empleado, proyecto_registrado)
                    key_historia = str(histroia_usuario['key'])
                    funcionalidad = funcionalidad

                    actividad = Actividad.objects.create(
                            identificador=key_historia,
                            proyecto_empleado=proyecto_empleado,
                            funcionalidad=funcionalidad,
                            tiempo_estimado=histroia_usuario['tiempo_estimado'],
                            tiempo_real=histroia_usuario['tiempo_total'],
                            slug_tipos=''
                        )
            except Exception as e:
                print("Errro", e)


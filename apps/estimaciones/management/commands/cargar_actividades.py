from apps.estimaciones.models.actividades import Actividad
from django.core.management.base import BaseCommand

from apps.prueba.utils import GestorLectorExcel

from apps.estimaciones.models.tipos_actividades import TipoActividad
from apps.estimaciones.models.proyectos import Proyecto
from apps.estimaciones.models.proyectos_empleados import ProyectoEmpleado

from apps.usuarios.models.empleados import Empleado


class Command(BaseCommand):
    help = 'Carga los datos iniciales de las historias de usuario desde un archivo Excel'

    def handle(self, *args, **kwargs):

        gestor = GestorLectorExcel("F:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\Jira_kairosteam.xlsx")

        data_frame = gestor.obtener_dataframe().fillna(0)

        for index, row in data_frame.iterrows():
            try:
                tipo_actividad = TipoActividad.buscar_por_nombre(row['Summary'])
                proyecto = Proyecto.buscar_por_nombre(row['Proyecto'].capitalize())
                empleado = Empleado.buscar_por_username(row['Correo'])
                if empleado:
                    proyecto_empleado = ProyectoEmpleado.crear_y_obtener(empleado, proyecto)
                    key_historia = str(row['Issue key'])
                    funcionalidad = str(row['Descripcion'])

                    tiempo_estimado = float(row['Original estimate']/60)
                    tiempo_real = float(row['Time Spent']/60)

                    Actividad.objects.create(
                        tipo_actividad=tipo_actividad,
                        identificador=key_historia,
                        proyecto_empleado=proyecto_empleado,
                        funcionalidad=funcionalidad,
                        tiempo_estimado=tiempo_estimado,
                        tiempo_real=tiempo_real
                    )
                else:
                    print("Programador inexistente")
            except Exception as e:
                print("Errro", e)
        

from apps.estimaciones.models.actividades import Actividad
from django.core.management.base import BaseCommand

from apps.prueba.utils import GestorLectorExcel

from apps.estimaciones.models.tipos_actividades import TipoActividad
from apps.estimaciones.models.proyectos import Proyecto
from apps.estimaciones.models.proyecto_programador import ProyectoProgramador

from apps.usuarios.models.programadores import Programador


class Command(BaseCommand):
    help = 'Carga los datos iniciales de los productos'

    def handle(self, *args, **kwargs):

        gestor = GestorLectorExcel("F:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\Jira_kairosteam.xlsx")

        data_frame = gestor.obtener_dataframe().fillna(0)
        for index, row in data_frame.iterrows():
            try:
                tipo_actividad = TipoActividad.buscar_por_nombre(row['Summary'])
                proyecto = Proyecto.buscar_por_nombre(row['Proyecto'].capitalize())
                proramador = Programador.buscar_por_username(row['Assignee'])

                proyecto_programador = ProyectoProgramador.crear_y_obtener(proramador, proyecto)
                funcionalidad = str(row['Descripcion'])

                tiempo_estimado = float(row['Original estimate']/60)
                tiempo_real = float(row['Time Spent']/60)

                Actividad.objects.create(
                    tipo_actividad=tipo_actividad,
                    proyecto_programador=proyecto_programador,
                    funcionalidad=funcionalidad,
                    tiempo_estimado=tiempo_estimado,
                    tiempo_real=tiempo_real
                )
            except:
                print("Errro")

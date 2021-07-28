from django.core.management.base import BaseCommand

from apps.prueba.utils import GestorLectorExcel

from ...models.tipos_actividades import TipoActividad
from ...models.estructuras import Estructura
from apps.actividades.models import estructuras

class Command(BaseCommand):
    help = 'Carga los datos iniciales de los productos'

    def handle(self, *args, **kwargs):
        
        gestor = GestorLectorExcel("F:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\jira_actividades.xlsx")
        
        data_frame = gestor.obtener_dataframe()

        data_frame = gestor.obtener_dataframe().fillna(0)

        lugar = Estructura.obtener_estructura_lugar()
        accion = Estructura.obtener_estructura_accion()
        tarea = Estructura.obtener_estructura_tarea()
        adicional = Estructura.obtener_estructura_adicional()

        for index, row in data_frame.iterrows():
            

                      

            if TipoActividad.existe_por_nombre(row['Tipo_uno']) == False:
                tipo_actividad_1 = TipoActividad.objects.create(nombre=row['Tipo_uno'], estructura=lugar)

            if TipoActividad.existe_por_nombre(row['Tipo_dos']) == False:
                tipo_actividad_2 = TipoActividad.objects.create(nombre=row['Tipo_dos'], estructura=accion)

            if TipoActividad.existe_por_nombre(row['Tipo_tres']) == False:
                tipo_actividad_3 = TipoActividad.objects.create(nombre=row['Tipo_tres'], estructura=tarea)

from django.core.management.base import BaseCommand

from apps.prueba.utils import GestorLectorExcel

from apps.estimaciones.models.tipos_actividades import TipoActividad



class Command(BaseCommand):
    help = 'Carga los datos iniciales de los productos'

    def handle(self, *args, **kwargs):
        
        gestor = GestorLectorExcel("F:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\Jira_kairosteam.xlsx")
        
        
        data_frame = gestor.obtener_dataframe()
        lista_tipos = data_frame['Summary'].unique()
        for tipo in lista_tipos:
            if tipo != 'nan':
                TipoActividad.objects.create(nombre=tipo)

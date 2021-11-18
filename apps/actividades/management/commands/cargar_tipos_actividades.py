from django.core.management.base import BaseCommand

from apps.utils.clases.pandas import GestorLectorExcel

from ...models.tipos_actividades import TipoActividad

class Command(BaseCommand):
    help = 'Carga los datos iniciales de los productos'

    def handle(self, *args, **kwargs):
        
        gestor = GestorLectorExcel("G:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\Jira_kairosteam.xlsx")
        
        data_frame = gestor.obtener_dataframe()
        print("##############################")
        
        lista_tipos = data_frame['Summary'].unique()
        print(lista_tipos)
        for tipo in lista_tipos:
            if tipo != 'nan':
                TipoActividad.objects.create(nombre=tipo)

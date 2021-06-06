# Modulos Django
from django.shortcuts import render
from django.views.generic import TemplateView

# Modulos de otras apps

# Modulos apps propias
from apps.prueba.utils import GestorLectorExcel

# Create your views here.
class TablerosHoras(TemplateView):
    template_name = "pruebas/prueba.html"

    def get_context_data(self, **kwargs):
        data = super(TablerosHoras, self).get_context_data(**kwargs)
        gestor = GestorLectorExcel("F:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\Jira_kairosteam.xlsx")
        
        
        lista_datos = gestor.obtener_descripcion_columna('Summary', 'Time spent(Horas)')         
        graficas_cantidad = {'nombre':'grafica_cantidad', 'grafica':gestor.contar_cantidad_repetidos('Summary')}
        graficas_tiempo = {'nombre':'grafica_tiempo', 'grafica':gestor.sumar_valores_agrupados('Summary', 'Time spent(Horas)')}
        lista_datos_compuestos = {'nombre':'grafica_cantidad_tiempo', 'grafica':gestor.obtener_cantidad_y_suma('Summary', 'Time spent(Horas)', 12)}
        data['graficas'] = [lista_datos_compuestos]        
        data['lista_datos'] = lista_datos
       
        print(lista_datos_compuestos)
        
        
        return data
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from rest_framework.views import APIView
from rest_framework.response import Response
from config.settings.base import DIRECCION_HOST

from apps.estimaciones.forms import RegistrarActividadForm
from apps.estimaciones.models.actividades import Actividad
from apps.utils.clases.pandas.gestor_pandas import (
    GestorLectorQueryset,
    eliminar_ceros,
    eliminar_valores_atipicos,
    obtener_describe_dataframe,
)
from apps.utils.mixin import MensajeMixin

import pandas as pd

class RegistrarActividad(MensajeMixin, CreateView):
    model = Actividad
    form_class = RegistrarActividadForm
    success_url = reverse_lazy("estimaciones:listado_actividades")
    template_name = "estimaciones/actividades/registrar.html"
    mensaje_exito = "La actividad ha sido registrada correctamente"
    mensaje_error = "Error registrar actividad, por favor verificar los datos"


class ListadoActividad(ListView):
    model = Actividad
    context_object_name = "actividades"
    template_name = "estimaciones/actividades/listado.html"


class ObtenerActividadesComunes(APIView):

    def get(self, request):
        parametros = self.request.GET

        nombre = parametros["nombre"]
        actividades = list(Actividad.obtener_actividades_por_nombre(nombre))

        lector = GestorLectorQueryset(actividades)
        df = lector.obtener_dataframe()
        df = eliminar_ceros(df)
        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_real')
        lista_de_estimaciones = obtener_describe_dataframe(df_sin_atipicos, ['tipo_actividad__nombre'], 'tiempo_real')

        print(lista_de_estimaciones)
        return Response({
            "actividades": lista_de_estimaciones,
        })



    """def obtener_valores_columna(self, columna:str) -> 'list<str>':
        return self._dataframe[columna].unique().tolist()


    def obtener_descripcion_columna(self, columna_datos:str, columna_info:str):
        lista_datos = list()
        lista_valores = self.obtener_valores_columna(columna_datos)
        for valor in lista_valores:
            
            df = self._dataframe[self._dataframe[columna_datos].isin([valor])]
            df = df[[columna_datos, columna_info, 'Issue key']]
            df = self.eliminar_ceros(df)
            df_atipicos = self.obtener_valores_atipicos(df, columna_info)
            df_sin_atipicos = self.eliminar_valores_atipicos(df, columna_info)
            
            if not df.empty:
                lista_datos.append({'valor':valor, 'descripcion':df_sin_atipicos[columna_info].describe()})
        return lista_datos"""
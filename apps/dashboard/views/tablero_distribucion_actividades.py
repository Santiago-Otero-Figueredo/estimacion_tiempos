from braces.views import LoginRequiredMixin
from django.views.generic.edit import FormView

from apps.actividades.models.actividades import Actividad
from ..forms import FiltroTablerosForm

from apps.utils.clases.pandas.gestor_pandas import (
    GestorLectorQueryset,
    eliminar_ceros,
    eliminar_valores_atipicos,
    obtener_suma_columna,
    obtener_suma_columna_agrupada,
    obtener_data_frame_por_valor_en_columna,
)


class TableroDistribucion(LoginRequiredMixin, FormView):
    form_class = FiltroTablerosForm
    template_name = "dashboard/distribucion_actividades.html"

    def get_context_data(self, **kwargs) -> 'QuerySet[T]':
        context = super().get_context_data(**kwargs)
        filtros = self.aplicar_filtros()

        actividades = Actividad.obtener_todos().filter(
                    tipos_actividades__isnull=False,
                    proyecto_empleado__isnull=False,
                ).filter(**filtros).values(
                    'proyecto_empleado__proyecto__nombre',
                    'tipos_actividades__nombre',
                    'tiempo_estimado',
                    'tiempo_real',
                    'slug_tipos'
                )

        context['lista_distribucion_actividades'] = self.obtener_informacion_grafica(actividades)['lista_proyectos']
        context['proyectos'] = self.obtener_informacion_grafica(actividades)['proyectos']
        return context

    def obtener_informacion_grafica(self, actividades):
        
        proyectos = set(actividades.values_list('proyecto_empleado__proyecto__nombre', flat=True))


        lector = GestorLectorQueryset(list(actividades))
        df = lector.obtener_dataframe()
        df = eliminar_ceros(df)
        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_real')
        lista_proyectos = list()
        for proyecto in proyectos:
            dataframe_proyecto = obtener_data_frame_por_valor_en_columna(df_sin_atipicos, 'proyecto_empleado__proyecto__nombre', proyecto)
            lista_de_tiempos_reales = obtener_suma_columna_agrupada(dataframe_proyecto, ['proyecto_empleado__proyecto__nombre', 'slug_tipos'], 'tiempo_real', 5)
            tiempo_total = obtener_suma_columna(dataframe_proyecto, 'tiempo_real')

            diccionario_proyecto = dict()
            diccionario_proyecto['category'] = proyecto
            for tipo, informacion_real in lista_de_tiempos_reales.items():
                porcentaje_participacion = informacion_real.pop('tiempo_total', 0)
                diccionario_proyecto[tipo[1]] = porcentaje_participacion
            lista_proyectos.append(diccionario_proyecto)
       
        return {'lista_proyectos':lista_proyectos, 'proyectos':list(proyectos)}


    def get_initial(self):
        initial = super().get_initial()

        if 'proyecto' in self.request.GET:
            initial['proyecto'] = self.request.GET.getlist('proyecto')
        if 'empleado' in self.request.GET:
            initial['empleado'] = self.request.GET['empleado']
        return initial

    def aplicar_filtros(self):
        filtro = dict()
        if 'proyecto' in self.request.GET and not self.request.GET["proyecto"] == "":
            filtro['proyecto_empleado__proyecto__pk__in'] = self.request.GET.getlist('proyecto')
        if 'empleado' in self.request.GET and not self.request.GET["empleado"] == "":
            filtro['proyecto_empleado__empleado__pk'] = self.request.GET['empleado']
        return filtro


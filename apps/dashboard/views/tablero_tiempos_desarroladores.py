from apps.actividades.models.estructuras import Estructura
from braces.views import LoginRequiredMixin
from django.views.generic.edit import FormView

from apps.actividades.models.actividades import Actividad
from ..forms import FiltroEstimacionesTiemposForm

from apps.utils.clases.pandas.gestor_pandas import (
    GestorLectorQueryset,
    eliminar_ceros,
    eliminar_valores_atipicos,
    obtener_describe_dataframe,
)


class TableroTiempos(LoginRequiredMixin, FormView):
    form_class = FiltroEstimacionesTiemposForm
    template_name = "dashboard/tiempo_desarrolladores.html"

    def get_context_data(self, **kwargs) -> 'QuerySet[T]':
        context = super().get_context_data(**kwargs)
        filtros = self.aplicar_filtros()

        filtros_lugares = filtros.pop('tipos_lugares', Estructura.obtener_actividades_lugar().values_list('pk', flat=True))
        filtros_acciones = filtros.pop('tipos_acciones', Estructura.obtener_actividades_accion().values_list('pk', flat=True))
        filtros_tareas = filtros.pop('tipos_tareas', Estructura.obtener_actividades_tarea().values_list('pk', flat=True))

        actividades = Actividad.obtener_todos().filter(
                    tipos_actividades__isnull=False,
                    proyecto_empleado__isnull=False,
                ).filter(
                    tipos_actividades__pk__in=filtros_lugares
                ).filter(
                    tipos_actividades__pk__in=filtros_acciones
                ).filter(
                    tipos_actividades__pk__in=filtros_tareas
                ).filter(**filtros).values(
                    'proyecto_empleado__empleado__first_name',
                    'tipos_actividades__nombre',
                    'tiempo_estimado',
                    'tiempo_real',
                    'slug_tipos'
                )

        context['lista_tiempos_desarrolladores'] = self.obtener_informacion_grafica(actividades)
        return context

    def obtener_informacion_grafica(self, actividades):

        lector = GestorLectorQueryset(list(actividades))
        df = lector.obtener_dataframe()
        df = eliminar_ceros(df)
        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_real')
        
        lista_de_tiempos_reales = obtener_describe_dataframe(df_sin_atipicos, ['proyecto_empleado__empleado__first_name'], 'tiempo_real')
        lista_tiempos_desarrollador = list()
        for desarrollador, tiempo in lista_de_tiempos_reales.items():
            print(desarrollador,tiempo)
            lista_tiempos_desarrollador.append(
                {
                    "elemento_eje_X": desarrollador,
                    "open": tiempo['cuartil_1'],
                    "high": tiempo['maximo'],
                    "low": tiempo['minimo'],
                    "close": tiempo['cuartil_3']
                }
            )

        return lista_tiempos_desarrollador


    def get_initial(self):
        initial = super().get_initial()

        if 'proyecto' in self.request.GET:
            initial['proyecto'] = self.request.GET.getlist('proyecto')
        if 'empleado' in self.request.GET:
            initial['empleado'] = self.request.GET['empleado']

        if 'tipos_lugares' in self.request.GET:
            initial['tipos_lugares'] = self.request.GET.getlist('tipos_lugares')
        if 'tipos_acciones' in self.request.GET:
            initial['tipos_acciones'] = self.request.GET.getlist('tipos_acciones')
        if 'tipos_tareas' in self.request.GET:
            initial['tipos_tareas'] = self.request.GET.getlist('tipos_tareas')
        return initial

    def aplicar_filtros(self):
        filtro = dict()
        if 'proyecto' in self.request.GET and not self.request.GET["proyecto"] == "":
            filtro['proyecto_empleado__proyecto__pk__in'] = self.request.GET.getlist('proyecto')
        if 'empleado' in self.request.GET and not self.request.GET["empleado"] == "":
            filtro['proyecto_empleado__empleado__pk'] = self.request.GET['empleado']

        if 'tipos_lugares' in self.request.GET:
            filtro['tipos_lugares'] = self.request.GET.getlist('tipos_lugares')
        if 'tipos_acciones' in self.request.GET:
            filtro['tipos_acciones'] = self.request.GET.getlist('tipos_acciones')
        if 'tipos_tareas' in self.request.GET:
            filtro['tipos_tareas'] = self.request.GET.getlist('tipos_tareas')

        return filtro


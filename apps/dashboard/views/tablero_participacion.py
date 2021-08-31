
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import Cast
from django.db.models import FloatField
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
)


class TableroParticipacion(LoginRequiredMixin, FormView):
    form_class = FiltroTablerosForm
    template_name = "dashboard/tablero_participacion.html"

    def get_context_data(self, **kwargs) -> 'QuerySet[T]':
        context = super().get_context_data(**kwargs)
        filtros = self.aplicar_filtros()

        actividades = Actividad.obtener_todos().filter(
                    tipos_actividades__isnull=False,
                    proyecto_empleado__isnull=False,
                ).filter(**filtros).values(
                    'tipos_actividades__nombre',
                    'tiempo_estimado',
                    'tiempo_real',
                    'slug_tipos'
                )
        
        context['lista_descripcion_tiempos'] = self.obtener_informacion_grafica(actividades)
        context['lista_informacion_proyectos'] = self.obtener_informacion_tabla(actividades)
        return context

    def obtener_informacion_tabla(self, actividades):
        actividades_agrupadas = actividades.values('proyecto_empleado__proyecto__nombre').annotate(
            empleados=Count('proyecto_empleado__empleado', distinct=True), 
            tiempo_estimado=Cast(Sum('tiempo_estimado'), FloatField())/60.0, 
            tiempo_real=Cast(Sum('tiempo_real'), FloatField())/60.0
        ).order_by()

        return list(actividades_agrupadas)

    def obtener_informacion_grafica(self, actividades):

        lector = GestorLectorQueryset(list(actividades))
        df = lector.obtener_dataframe()
        df = eliminar_ceros(df)
        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_real')
        lista_de_tiempos_reales = obtener_suma_columna_agrupada(df_sin_atipicos, ['slug_tipos'], 'tiempo_real')

        tiempo_total = obtener_suma_columna(df_sin_atipicos, 'tiempo_real')

        lista_descripcion_tiempos = list()
        for tipo, informacion_real in lista_de_tiempos_reales.items():
            porcentaje_participacion = (informacion_real.pop('tiempo_total', 0)/tiempo_total)*100
            lista_descripcion_tiempos.append(
                {
                    'nombre':tipo,
                    'cantidad':porcentaje_participacion,
                }
            )
        return lista_descripcion_tiempos


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


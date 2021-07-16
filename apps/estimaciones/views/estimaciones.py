from django.views.generic.edit import FormView

from apps.actividades.models.actividades import Actividad
from apps.estimaciones.forms.estimaciones import FiltroEstimacionesForm
from apps.utils.clases.pandas.gestor_pandas import (
    GestorLectorQueryset,
    eliminar_ceros,
    eliminar_valores_atipicos,
    obtener_describe_dataframe,
)


class ObtenerEstimacionesActividades(FormView):
    form_class = FiltroEstimacionesForm
    template_name = "estimaciones/estimaciones/listado.html"
    context_object_name = "actividades"

    def get_context_data(self, **kwargs) -> 'QuerySet[T]':
        context = super().get_context_data(**kwargs)
        filtros = self.aplicar_filtros()
        print(filtros)
        actividades = list(Actividad.obtener_todos().filter(**filtros).values(
            #'proyecto_programador__proyecto__nombre',
            #'proyecto_programador__proyecto__cliente__first_name',
            #'proyecto_programador__proyecto__programadores',
            'tipo_actividad__nombre',
            #'fecha_inicio',
            #'fecha_finalizacion',
            'tiempo_estimado',
            'tiempo_real'
            )
        )

        lector = GestorLectorQueryset(actividades)
        df = lector.obtener_dataframe()
        df = eliminar_ceros(df)
        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_real')
        lista_de_tiempos_reales = obtener_describe_dataframe(df_sin_atipicos, ['tipo_actividad__nombre'], 'tiempo_real')

        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_estimado')
        lista_de_estimaciones = obtener_describe_dataframe(df_sin_atipicos, ['tipo_actividad__nombre'], 'tiempo_estimado')

        lista_descripcion_tiempos = list()
        for tipo, informacion_real in lista_de_tiempos_reales.items():
            informacion_estimacion = lista_de_estimaciones.pop(tipo,dict())
            lista_descripcion_tiempos.append(
                {
                    'nombre':tipo,
                    'cantidad':informacion_real.pop('cantidad', 0),
                    'promedio':{
                        'estimado':informacion_real.pop('promedio','-'),
                        'real':informacion_estimacion.pop('promedio','-'),
                    },
                    'minimo':{
                        'estimado':informacion_real.pop('minimo','-'),
                        'real':informacion_estimacion.pop('minimo','-'),
                    },
                    'maximo':{
                        'estimado':informacion_real.pop('maximo','-'),
                        'real':informacion_estimacion.pop('maximo','-'),
                    },
                    'desviacion':{
                        'estimado':informacion_real.pop('desviacion','-'),
                        'real':informacion_estimacion.pop('desviacion','-'),
                    }
                }
            )
        context['tipos_actividades'] = lista_descripcion_tiempos
        return context

    def get_initial(self):
        initial = super().get_initial()

        if 'proyecto' in self.request.GET:
            initial['proyecto'] = self.request.GET['proyecto']
        if 'empleado' in self.request.GET:
            initial['empleado'] = self.request.GET['empleado']
        if 'tipo_actividad' in self.request.GET:
            initial['tipo_actividad'] = self.request.GET['tipo_actividad']
        if 'fecha_inicio' in self.request.GET:
            initial['fecha_inicio'] = self.request.GET['fecha_inicio']
        if 'fecha_fin' in self.request.GET:
            initial['fecha_fin'] = self.request.GET['fecha_fin']
        return initial

    def aplicar_filtros(self):
        filtro = dict()
        if 'proyecto' in self.request.GET and not self.request.GET["proyecto"] == "":
            filtro['proyecto_empleado__proyecto__pk'] = self.request.GET['proyecto']
        if 'empleado' in self.request.GET and not self.request.GET["empleado"] == "":
            filtro['proyecto_empleado__empleado__pk'] = self.request.GET['empleado']
        if 'tipo_actividad' in self.request.GET and not self.request.GET["tipo_actividad"] == "":
            filtro['tipo_actividad__pk'] = self.request.GET['tipo_actividad']
        if 'fecha_inicio' in self.request.GET and not self.request.GET["fecha_inicio"] == "":
            filtro['fecha_inicio__gte'] = self.request.GET['fecha_inicio']
        if 'fecha_fin' in self.request.GET and not self.request.GET["fecha_fin"] == "":
            filtro['fecha_finalizacion__lte'] = self.request.GET['fecha_fin']
        return filtro



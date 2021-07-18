from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormView

from rest_framework.views import APIView
from rest_framework.response import Response

from ..forms import (RegistrarActividadForm,
                     FiltroElementosJIRAForm)
from ..models.actividades import Actividad

from apps.utils.clases.pandas.gestor_pandas import (
    GestorLectorQueryset,
    eliminar_ceros,
    eliminar_valores_atipicos,
    obtener_describe_dataframe,
)

from apps.utils.mixin import MensajeMixin
from apps.utils.clases.jira.ConexionJira import Jira

from braces.views import LoginRequiredMixin

class RegistrarActividad(MensajeMixin, CreateView):
    model = Actividad
    form_class = RegistrarActividadForm
    success_url = reverse_lazy("actividades:listado_actividades")
    template_name = "actividades/actividades/registrar.html"
    mensaje_exito = "La actividad ha sido registrada correctamente"
    mensaje_error = "Error al registrar actividad, por favor verificar los datos"


class ModificarActividad(LoginRequiredMixin, UpdateView):
    model = Actividad
    form_class = RegistrarActividadForm
    template_name = "actividades/actividades/modificar.html"
    success_url = reverse_lazy("actividades:listado_actividades")
    mensaje_exito = "La actividad ha sido modificada correctamente"
    mensaje_error = "Error al modificada actividad, por favor verificar los datos"


class ListadoActividad(ListView):
    model = Actividad
    context_object_name = "actividades"
    template_name = "actividades/actividades/listado.html"


class ImportarActividadesJIRA(FormView):
    form_class = FiltroElementosJIRAForm
    success_url = reverse_lazy("actividades:importar_actividades_jira")
    template_name = "actividades/actividades/importar_jira.html"

    def obtener_lista_proyectos_en_tupla(self):
        
        lista_proyectos = self.jira.consultar_todos_los_proyectos()
        lista_retorno = list()
        for proyecto in lista_proyectos:
            lista_retorno.append(
                (proyecto['key'], proyecto['nombre'])
            )
        return tuple(lista_retorno)

    def dispatch(self, request, *args, **kwargs):
        self.jira = Jira()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['proyectos'] = self.obtener_lista_proyectos_en_tupla()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtros = self.aplicar_filtros()

        nombre_proyecto = filtros.pop('nombre_proyecto', '')
        print(nombre_proyecto,"##################")
        context['actividades'] = self.jira.consultar_historias_usuarios(nombre_proyecto)
        return context

    def get_initial(self):
        initial = super().get_initial()

        if 'nombre_proyecto' in self.request.GET:
            initial['nombre_proyecto'] = self.request.GET['nombre_proyecto']
        return initial

    def aplicar_filtros(self):
        filtro = dict()
        if 'nombre_proyecto' in self.request.GET and not self.request.GET["nombre_proyecto"] == "":
            filtro['nombre_proyecto'] = self.request.GET['nombre_proyecto']
        return filtro


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

        return Response({
            "actividades": lista_de_estimaciones,
        })

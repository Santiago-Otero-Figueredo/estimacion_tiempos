from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormView

from rest_framework.views import APIView
from rest_framework.response import Response

from ..forms import (RegistrarActividadForm,
                     FiltroElementosJIRAForm,
                     AsignarActividadForm,
                     AsignarActividadFormSet)
from ..models.actividades import Actividad
from ..models.caminos_actividades import CaminoActividad
from ..utils import crear_slug_tipos_actividad

from apps.utils.clases.pandas.gestor_pandas import (
    GestorLectorQueryset,
    eliminar_ceros,
    eliminar_valores_atipicos,
    obtener_describe_dataframe,
)

from apps.utils.mixin import MensajeMixin
from apps.utils.clases.jira.ConexionJira import Jira

from braces.views import LoginRequiredMixin

class RegistrarActividad(LoginRequiredMixin, MensajeMixin, CreateView):
    model = Actividad
    form_class = RegistrarActividadForm
    success_url = reverse_lazy("actividades:listado_actividades")
    template_name = "actividades/actividades/registrar.html"
    mensaje_exito = "La actividad ha sido registrada correctamente"
    mensaje_error = "Error al registrar actividad, por favor verificar los datos"


    def form_valid(self, form):
        elemento = form.save(commit=False)
        elemento.esta_activo = True
        elemento.save()

        tipos_lugares = form.cleaned_data['tipos_lugares']
        tipos_acciones = form.cleaned_data['tipos_acciones']
        tipos_tareas = form.cleaned_data['tipos_tareas']

        elemento.tipos_actividades.add(tipos_lugares)
        elemento.tipos_actividades.add(tipos_acciones)
        elemento.tipos_actividades.add(tipos_tareas)

        slug_tipos = crear_slug_tipos_actividad(
                        tipos_lugares.nombre,
                        tipos_acciones.nombre,
                        tipos_tareas.nombre,
                    )
        elemento.slug_tipos = slug_tipos
        elemento.save()
        return super().form_valid(form)

class ModificarActividad(LoginRequiredMixin, MensajeMixin, UpdateView):
    model = Actividad
    form_class = RegistrarActividadForm
    template_name = "actividades/actividades/modificar.html"
    success_url = reverse_lazy("actividades:listado_actividades")
    mensaje_exito = "La actividad ha sido modificada correctamente"
    mensaje_error = "Error al modificada actividad, por favor verificar los datos"

    def form_valid(self, form):
        elemento = form.save(commit=False)

        tipos_lugares = form.cleaned_data['tipos_lugares']
        tipos_acciones = form.cleaned_data['tipos_acciones']
        tipos_tareas = form.cleaned_data['tipos_tareas']

        lista_caminos = self.get_object().tipos_actividades.values_list('pk', flat=True)
        caminos = CaminoActividad.objects.filter(
            actividad=elemento,
            tipo_actividad__pk__in=lista_caminos
        )
        caminos.delete()
        elemento.tipos_actividades.add(tipos_lugares)
        elemento.tipos_actividades.add(tipos_acciones)
        elemento.tipos_actividades.add(tipos_tareas)

        slug_tipos = crear_slug_tipos_actividad(
                        tipos_lugares.nombre,
                        tipos_acciones.nombre,
                        tipos_tareas.nombre,
                    )

        elemento.slug_tipos = slug_tipos
        elemento.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        tipos = self.get_object().tipos_actividades.all().order_by('estructura__pk')
        initial['tipos_lugares'] = tipos[0]
        initial['tipos_acciones'] = tipos[1]
        initial['tipos_tareas'] = tipos[2]
        return initial



class ListadoActividad(LoginRequiredMixin, ListView):
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
        if 'filtro' in self.request.GET:
            print("filtro")
            context['actividades'] = self.jira.consultar_historias_usuarios(nombre_proyecto)
        elif 'importar' in self.request.GET:
            print("IMPORTAR")
            jira = Jira()
            proyecto = self.request.GET['nombre_proyecto']
            jira.cargar_actividades_de_proyecto(proyecto)
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



class AsociarActividadesSinTipos(LoginRequiredMixin, MensajeMixin, FormView):
    model = Actividad
    form_class = AsignarActividadForm
    success_url = reverse_lazy("actividades:listado_actividades")
    template_name = "actividades/actividades/asignar_actividad.html"
    mensaje_exito = "Tipos de actividades asociados correctamente"
    mensaje_error = "Error al asociar tipo de actividad a las actividades, por favor verificar los datos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_estructuras = AsignarActividadFormSet(queryset=Actividad.obtener_actividades_sin_tipos(), prefix="actividades")
        self.formset_estructuras.extra = 0

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = self.formset_estructuras
        return data

    def post(self, *args, **kwargs):

        formset = AsignarActividadFormSet(self.request.POST, prefix="actividades")

        if formset.is_valid():
            self.form_valid(self.get_form())
            return self.formset_valid(formset)
        else:
            errores = ''
            for form in formset:
                for _, errors in form.errors.items():
                    errores += ('{}'.format(','.join(errors)))
            messages.error(self.request, "{}, {}".format(self.mensaje_error,errores))
            return redirect('actividades:listado_actividades')

    def formset_valid(self, formset):

        for form in formset:
            registrar = form.cleaned_data['registrar']
            if registrar:
                actividad = form.save(commit=False)
                tipos_lugares = form.cleaned_data['tipos_lugares']
                tipos_acciones = form.cleaned_data['tipos_acciones']
                tipos_tareas = form.cleaned_data['tipos_tareas']

                actividad.identificador = form.instance.identificador
                actividad.funcionalidad = form.instance.funcionalidad

                lista_caminos = actividad.tipos_actividades.values_list('pk', flat=True)
                caminos = CaminoActividad.objects.filter(
                    actividad=actividad,
                    tipo_actividad__pk__in=lista_caminos
                )
                caminos.delete()
                actividad.tipos_actividades.add(tipos_lugares)
                actividad.tipos_actividades.add(tipos_acciones)
                actividad.tipos_actividades.add(tipos_tareas)

                slug_tipos = crear_slug_tipos_actividad(
                        tipos_lugares.nombre,
                        tipos_acciones.nombre,
                        tipos_tareas.nombre,
                    )

                actividad.slug_tipos = slug_tipos
                actividad.save()
            
        return self.form_valid(self.get_form())


class ObtenerActividadesComunes(APIView):

    def get(self, request):
        parametros = self.request.GET

        nombre = parametros["nombre"]
        actividades = list(Actividad.obtener_actividades_por_nombre(nombre))

        lector = GestorLectorQueryset(actividades)
        df = lector.obtener_dataframe()
        
        df = eliminar_ceros(df)
        df_sin_atipicos = eliminar_valores_atipicos(df, 'tiempo_real')

        lista_de_estimaciones = obtener_describe_dataframe(df_sin_atipicos, ['slug_tipos'], 'tiempo_real')

        return Response({
            "actividades": lista_de_estimaciones,
        })

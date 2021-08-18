from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import TemplateView

from ..models.proyectos import Proyecto
from ..models.contactos_proyecto import ContactoProyecto
from ..forms import (RegistrarProyectoForm,
                     ContactoFormSet)

from apps.utils.mixin import MensajeMixin
from apps.utils.clases.jira.ConexionJira import Jira

from braces.views import LoginRequiredMixin

class RegistrarProyecto(LoginRequiredMixin, MensajeMixin, CreateView):
    model = Proyecto
    form_class = RegistrarProyectoForm
    success_url = reverse_lazy("proyectos:listado_proyectos")
    template_name = "proyectos/proyectos/registrar.html"
    mensaje_exito = "Proyecto registrado correctamente"
    mensaje_error = "Error al registrar el proyecto, por favor verificar los datos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_estructuras = ContactoFormSet(queryset=ContactoProyecto.objects.none(), prefix="contacto")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = self.formset_estructuras
        return data

    def post(self, *args, **kwargs):

        formset = ContactoFormSet(self.request.POST, prefix="contacto")

        if formset.is_valid():
            self.form_valid(self.get_form())
            return self.formset_valid(formset)
        else:
            errores = ''
            for form in formset:
                for _, errors in form.errors.items():
                    errores += ('{}'.format(','.join(errors)))

            messages.error(self.request, "{}, {}".format(self.mensaje_error,errores))
            return redirect('proyectos:registrar_proyecto')

    def formset_valid(self, formset):

        for form in formset:
            contacto = form.save(commit=False)
            contacto.proyecto = self.object
            contacto.esta_activo = True
            contacto.save()
            
        return self.form_valid(self.get_form())


class ModificarProyecto(LoginRequiredMixin, MensajeMixin, UpdateView):
    model = Proyecto
    form_class = RegistrarProyectoForm
    template_name = "proyectos/proyectos/modificar.html"
    success_url = reverse_lazy("proyectos:listado_proyectos")
    mensaje_exito = "Proyecto modificado correctamente"
    mensaje_error = "Error al modificar el proyecto, por favor verificar los datos"


class ListadoProyecto(LoginRequiredMixin, ListView):
    model = Proyecto
    context_object_name = "proyectos"
    template_name = "proyectos/proyectos/listado.html"



class ImportarProyectosJIRA(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy("proyectos:listado_proyectos")
    template_name = "proyectos/proyectos/importar_jira.html"

    def dispatch(self, request, *args, **kwargs):
        self.jira = Jira()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyectos'] = self.jira.consultar_todos_los_proyectos()

        proyectos_registrados = list(Proyecto.obtener_todos().values_list('identificador_jira', flat=True))
        listado_proyectos_no_registrados = list()
        for proyecto in context['proyectos']:
            if not proyecto['key'] in proyectos_registrados:
                listado_proyectos_no_registrados.append(proyecto)
        
        context['proyectos'] = listado_proyectos_no_registrados
        if self.request.GET:
            for proyecto in context['proyectos']:
                if Proyecto.existe_por_identificador_jira(proyecto['key']) == False:
                    Proyecto.objects.create(
                        identificador_jira=proyecto['key'],
                        nombre=proyecto['nombre'],
                    )
        return context
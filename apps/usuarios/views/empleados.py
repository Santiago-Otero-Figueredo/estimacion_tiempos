from apps.usuarios.models.administradores import Administrador
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import  UpdateView


from apps.utils.clases.jira.ConexionJira import Jira
from apps.utils.mixin import MensajeMixin

from ..models.tipos_usuarios import TipoUsuario
from ..models.trabajadores import Trabajador
from ..models.empleados import Empleado
from ..forms.empleados import ModificarEmpleadoForm

from braces.views import LoginRequiredMixin


class ListadoEmpleados(LoginRequiredMixin, ListView):
    model = Empleado
    context_object_name = "empleados"
    template_name = "usuarios/empleados/listado.html"

    def get_queryset(self):
        return Empleado.obtener_empleados_sin_tipo()

class ModificarEmpleado(LoginRequiredMixin, MensajeMixin, UpdateView):
    model = Empleado
    form_class = ModificarEmpleadoForm
    template_name = "usuarios/empleados/modificar.html"
    success_url = reverse_lazy("usuarios:listado_empleados")
    mensaje_exito = "Empleado modificado correctamente"
    mensaje_error = "Error al modificar el empleado, por favor verificar los datos"

    def form_valid(self, form):
        elemento = form.save(commit=False)

        elemento_datos = {
            'pk':self.get_object().pk,
            'tipo_usuario':form.cleaned_data['tipo_usuario'],
            'tipo_documento':form.cleaned_data['tipo_documento'],
            'first_name':form.cleaned_data['first_name'],
            'last_name':form.cleaned_data['last_name'],
            'phone_number':form.cleaned_data['phone_number'],
            'numero_documento':form.cleaned_data['numero_documento'],
            'email':form.cleaned_data['email'],
            'creado':self.get_object().creado,
            'identificador_jira':self.get_object().identificador_jira
        }
        elemento.save()
        
        if form.cleaned_data['tipo_usuario'] == TipoUsuario.obtener_tipo_trabajador():
            Trabajador.objects.create(**elemento_datos)
        if form.cleaned_data['tipo_usuario'] == TipoUsuario.obtener_tipo_administrador():
            Administrador.objects.create(**elemento_datos)
        
        return redirect("usuarios:listado_empleados")

class ImportarEmpleadosJIRA(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy("usuarios:listado_trabajadores")
    template_name = "usuarios/empleados/importar_jira.html"

    def dispatch(self, request, *args, **kwargs):
        self.jira = Jira()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empleados'] = self.jira.consultar_todos_los_usuarios()

        if self.request.GET:
            for empleado in context['empleados']:
                Empleado.objects.create(
                    identificador_jira=empleado['accountId'],
                    first_name=empleado['displayName'],
                    username=empleado['accountId'],
                    email=empleado['accountId']
                )
        return context


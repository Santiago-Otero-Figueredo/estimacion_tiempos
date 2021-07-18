from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ..models.proyectos_empleados import ProyectoEmpleado
from ..forms import RegistrarProyectoEmpleadoForm

from apps.utils.mixin import MensajeMixin

from braces.views import LoginRequiredMixin

class RegistrarProyectoEmpleado(MensajeMixin, CreateView):
    model = ProyectoEmpleado
    form_class = RegistrarProyectoEmpleadoForm
    success_url = reverse_lazy("proyectos:listado_proyecto_empleados")
    template_name = "proyectos/proyectos_empleados/registrar.html"
    mensaje_exito = "El proyecto ha sido asignado al empleado correctamente"
    mensaje_error = "Error al asignar empleado al proyecto, por favor verificar los datos"


class ModificarProyectoEmpleado(LoginRequiredMixin, UpdateView):
    model = ProyectoEmpleado
    form_class = RegistrarProyectoEmpleadoForm
    template_name = "proyectos/proyectos_empleados/modificar.html"
    success_url = reverse_lazy("proyectos:listado_proyecto_empleados")
    mensaje_exito = "Se ha realizado la modificación correctamente"
    mensaje_error = "Error al realizar la modificación, por favor verificar los datos"


class ListadoProyectosEmpleados(ListView):
    model = ProyectoEmpleado
    context_object_name = "proyectos_empleados"
    template_name = "proyectos/proyectos_empleados/listado.html"
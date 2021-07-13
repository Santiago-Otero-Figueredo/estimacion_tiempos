from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.estimaciones.models.proyectos_empleados import ProyectoEmpleado
from apps.utils.mixin import MensajeMixin

from apps.estimaciones.forms import RegistrarProyectoEmpleadoForm

class RegistrarProyectoEmpleado(MensajeMixin, CreateView):
    model = ProyectoEmpleado
    form_class = RegistrarProyectoEmpleadoForm
    success_url = reverse_lazy("estimaciones:listado_proyectos_empleados")
    template_name = "estimaciones/proyectos_empleados/registrar.html"
    mensaje_exito = "El proyecto ha sido asignado al empleado correctamente"
    mensaje_error = "Error al asignar empleado al proyecto, por favor verificar los datos"


class ListadoProyectosEmpleados(ListView):
    model = ProyectoEmpleado
    context_object_name = "proyectos_empleados"
    template_name = "estimaciones/proyectos_empleados/listado.html"
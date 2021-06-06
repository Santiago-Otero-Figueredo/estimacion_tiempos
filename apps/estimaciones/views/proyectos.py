from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.estimaciones.models.proyectos import Proyecto
from apps.utils.mixin import MensajeMixin

from apps.estimaciones.forms import RegistrarProyectoForm

class RegistrarProyecto(MensajeMixin, CreateView):
    model = Proyecto
    form_class = RegistrarProyectoForm
    success_url = reverse_lazy("estimaciones:listado_proyectos")
    template_name = "estimaciones/proyectos/registrar.html"
    mensaje_exito = "Proyecto registrado correctamente"
    mensaje_error = "Error al registrar el proyecto, por favor verificar los datos"


class ListadoProyecto(ListView):
    model = Proyecto
    context_object_name = "proyectos"
    template_name = "estimaciones/proyectos/listado.html"
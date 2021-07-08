from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.estimaciones.models.proyecto_programador import ProyectoProgramador
from apps.utils.mixin import MensajeMixin

from apps.estimaciones.forms import RegistrarProyectoProgramadorForm

class RegistrarProyectoProgramador(MensajeMixin, CreateView):
    model = ProyectoProgramador
    form_class = RegistrarProyectoProgramadorForm
    success_url = reverse_lazy("estimaciones:listado_proyectos_programador")
    template_name = "estimaciones/proyectos_programador/registrar.html"
    mensaje_exito = "Proyecto ha sido asignado al programador correctamente"
    mensaje_error = "Error al asignar programador al proyecto, por favor verificar los datos"


class ListadoProyectoProgramador(ListView):
    model = ProyectoProgramador
    context_object_name = "proyectos_programador"
    template_name = "estimaciones/proyectos_programador/listado.html"
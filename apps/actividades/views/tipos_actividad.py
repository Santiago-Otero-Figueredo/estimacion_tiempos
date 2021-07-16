from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from ..models.tipos_actividades import TipoActividad
from ..forms import RegistrarTipoActividadForm

from apps.utils.mixin import MensajeMixin


class RegistrarTipoActividad(MensajeMixin, CreateView):
    model = TipoActividad
    form_class = RegistrarTipoActividadForm
    success_url = reverse_lazy("actividades:listado_tipos_actividades")
    template_name = "actividades/tipos_actividad/registrar.html"
    mensaje_exito = "El tipo de actividad ha sido registrada correctamente"
    mensaje_error = "Error registrar el tipo de actividad, por favor verificar los datos"


class ListadoTipoActividad(ListView):
    model = TipoActividad
    context_object_name = "tipos_actividad"
    template_name = "actividades/tipos_actividad/listado.html"
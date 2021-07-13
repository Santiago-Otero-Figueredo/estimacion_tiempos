from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.usuarios.models.trabajadores import Trabajador
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarTrabajadorForm

class RegistrarTrabajador(MensajeMixin, CreateView):
    model = Trabajador
    form_class = RegistrarTrabajadorForm
    success_url = reverse_lazy("usuarios:listado_trabajadores")
    template_name = "usuarios/trabajadores/registrar.html"
    mensaje_exito = "Trabajador registrado correctamente"
    mensaje_error = "Error al registrar el trabajador, por favor verificar los datos"


class ListadoTrabajadores(ListView):
    model = Trabajador
    context_object_name = "trabajadores"
    template_name = "usuarios/trabajadores/listado.html"
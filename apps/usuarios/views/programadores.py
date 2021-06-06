from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.usuarios.models.programadores import Programador
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarProgramadorForm

class RegistrarProgramador(MensajeMixin, CreateView):
    model = Programador
    form_class = RegistrarProgramadorForm
    success_url = reverse_lazy("usuarios:listado_programadores")
    template_name = "usuarios/programadores/registrar.html"
    mensaje_exito = "Programador registrado correctamente"
    mensaje_error = "Error al registrar el programador, por favor verificar los datos"


class ListadoProgramador(ListView):
    model = Programador
    context_object_name = "programadores"
    template_name = "usuarios/programadores/listado.html"
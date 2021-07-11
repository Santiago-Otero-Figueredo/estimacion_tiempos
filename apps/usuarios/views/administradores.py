from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.usuarios.models.administradores import Administrador
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarAdministradorForm

class RegistrarAdministrador(MensajeMixin, CreateView):
    model = Administrador
    form_class = RegistrarAdministradorForm
    success_url = reverse_lazy("usuarios:listado_administradores")
    template_name = "usuarios/administradores/registrar.html"
    mensaje_exito = "Administrador registrado correctamente"
    mensaje_error = "Error al registrar el administrador, por favor verificar los datos"


class ListadoAdministradores(ListView):
    model = Administrador
    context_object_name = "administradores"
    template_name = "usuarios/administradores/listado.html"
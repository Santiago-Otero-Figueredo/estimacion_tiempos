from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.usuarios.models.tipos_cargos import TipoCargo
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarCargoForm

class RegistrarCargo(MensajeMixin, CreateView):
    model = TipoCargo
    form_class = RegistrarCargoForm
    success_url = reverse_lazy("usuarios:listado_cargos")
    template_name = "usuarios/cargos/registrar.html"
    mensaje_exito = "Cargo registrado correctamente"
    mensaje_error = "Error al registrar el cargo, por favor verificar los datos"


class ListadoCargos(ListView):
    model = TipoCargo
    context_object_name = "cargos"
    template_name = "usuarios/cargos/listado.html"
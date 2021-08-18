from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.usuarios.models.tipos_cargos import TipoCargo
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarCargoForm

from braces.views import LoginRequiredMixin

class RegistrarCargo(LoginRequiredMixin, MensajeMixin, CreateView):
    model = TipoCargo
    form_class = RegistrarCargoForm
    success_url = reverse_lazy("usuarios:listado_cargos")
    template_name = "usuarios/cargos/registrar.html"
    mensaje_exito = "Cargo registrado correctamente"
    mensaje_error = "Error al registrar el cargo, por favor verificar los datos"


class ModificarCargo(LoginRequiredMixin, MensajeMixin, UpdateView):
    model = TipoCargo
    form_class = RegistrarCargoForm
    success_url = reverse_lazy("usuarios:listado_cargos")
    template_name = "usuarios/cargos/modificar.html"
    mensaje_exito = "Cargo modificado correctamente"
    mensaje_error = "Error al modificar el cargo, por favor verificar los datos"


class ListadoCargos(LoginRequiredMixin, ListView):
    model = TipoCargo
    context_object_name = "cargos"
    template_name = "usuarios/cargos/listado.html"
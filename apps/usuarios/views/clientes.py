from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.usuarios.models.clientes import Cliente
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarClienteForm

class RegistrarCliente(MensajeMixin, CreateView):
    model = Cliente
    form_class = RegistrarClienteForm
    success_url = reverse_lazy("usuarios:listado_clientes")
    template_name = "usuarios/clientes/registrar.html"
    mensaje_exito = "Cliente registrado correctamente"
    mensaje_error = "Error al registrar el cliente, por favor verificar los datos"


class ListadoCliente(ListView):
    model = Cliente
    context_object_name = "clientes"
    template_name = "usuarios/clientes/listado.html"
    

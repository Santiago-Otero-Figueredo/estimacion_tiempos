from django.views.generic import CreateView
from django.urls import reverse_lazy

from apps.usuarios.models.clientes import Cliente

from apps.usuarios.forms import RegistrarClienteForm

class RegistrarCliente(CreateView):
    model = Cliente
    form_class = RegistrarClienteForm
    template_name = "usuarios/clientes/registrar.html"
    

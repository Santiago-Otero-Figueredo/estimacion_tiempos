from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.usuarios.models.empresas import Empresa
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarEmpresaForm

class RegistrarEmpresa(MensajeMixin, CreateView):
    model = Empresa
    form_class = RegistrarEmpresaForm
    success_url = reverse_lazy("usuarios:listado_empresas")
    template_name = "usuarios/empresas/registrar.html"
    mensaje_exito = "Empresa registrada correctamente"
    mensaje_error = "Error al registrar la empresa, por favor verificar los datos"


class ListadoEmpresas(ListView):
    model = Empresa
    context_object_name = "empresa"
    template_name = "usuarios/empresas/listado.html"
    

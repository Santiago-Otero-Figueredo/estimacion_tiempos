from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ..models.empresas import Empresa
from ..models.tipos_documentos import TipoDocumento

from apps.utils.mixin import MensajeMixin
from apps.usuarios.forms import RegistrarEmpresaForm

from braces.views import LoginRequiredMixin


class RegistrarEmpresa(LoginRequiredMixin, MensajeMixin, CreateView):
    model = Empresa
    form_class = RegistrarEmpresaForm
    success_url = reverse_lazy("usuarios:listado_empresas")
    template_name = "usuarios/empresas/registrar.html"
    mensaje_exito = "Empresa registrada correctamente"
    mensaje_error = "Error al registrar la empresa, por favor verificar los datos"

    def get_initial(self):
        initial = super().get_initial()
        initial['tipo_documento'] = TipoDocumento.obtener_tipo_nit()
        return initial

class ModificarEmpresa(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = RegistrarEmpresaForm
    success_url = reverse_lazy("usuarios:listado_empresas")
    template_name = "usuarios/empresas/modificar.html"
    mensaje_exito = "Empresa modificada correctamente"
    mensaje_error = "Error al modificar la empresa, por favor verificar los datos"


class ListadoEmpresas(LoginRequiredMixin, ListView):
    model = Empresa
    context_object_name = "empresas"
    template_name = "usuarios/empresas/listado.html"
    

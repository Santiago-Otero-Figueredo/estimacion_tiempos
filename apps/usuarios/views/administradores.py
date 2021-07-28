from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ..models.administradores import Administrador
from ..models.tipos_documentos import TipoDocumento
from ..models.tipos_cargo_empelado import CargoEmpleado
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarAdministradorForm, ModificarAdministradorForm, AsignarCargoForm

from braces.views import LoginRequiredMixin

class RegistrarAdministrador(LoginRequiredMixin, MensajeMixin, CreateView):
    model = Administrador
    form_class = RegistrarAdministradorForm
    success_url = reverse_lazy("usuarios:listado_administradores")
    template_name = "usuarios/administradores/registrar.html"
    mensaje_exito = "Administrador registrado correctamente"
    mensaje_error = "Error al registrar el administrador, por favor verificar los datos"

    def form_valid(self, form):
        elemento = form.save(commit=False)
        elemento.save()
        elemento.cargos.add(form.cleaned_data['cargos'])

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['tipo_documento'] = TipoDocumento.obtener_tipo_cedula()
        return initial


class ModificarAdministrador(LoginRequiredMixin, MensajeMixin, UpdateView):
    model = Administrador
    form_class = ModificarAdministradorForm
    template_name = "usuarios/administradores/modificar.html"
    success_url = reverse_lazy("usuarios:listado_administradores")
    mensaje_exito = "Administrador modificado correctamente"
    mensaje_error = "Error al modificar el administrador, por favor verificar los datos"


class AsignarCargoAdministrador(LoginRequiredMixin, MensajeMixin, UpdateView):
    model = Administrador
    form_class = AsignarCargoForm
    template_name = "usuarios/administradores/asignar_cargo.html"
    success_url = reverse_lazy("usuarios:listado_administradores")
    mensaje_exito = "Cargo asignado a administrador correctamente"
    mensaje_error = "Error al asignar cargo al administrador, por favor verificar los datos"

    def get_initial(self):
        initial = super().get_initial()
        initial['cargos'] = self.get_object().obtener_ultimo_cargo()
        return initial

    def form_valid(self, form):
        elemento = form.save(commit=False)
        elemento.save()
        cargo_empleado = CargoEmpleado.buscar_por_empleado_y_cargo(elemento, form.cleaned_data['cargos'])
        if cargo_empleado:
            cargo_empleado.save()
        else:
            elemento.cargos.add(form.cleaned_data['cargos'])

        return redirect("usuarios:listado_administradores")


class ListadoAdministradores(LoginRequiredMixin, ListView):
    model = Administrador
    context_object_name = "administradores"
    template_name = "usuarios/administradores/listado.html"
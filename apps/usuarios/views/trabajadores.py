from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ..models.trabajadores import Trabajador
from ..models.tipos_documentos import TipoDocumento
from ..models.tipos_cargo_empelado import CargoEmpleado
from apps.utils.mixin import MensajeMixin

from apps.usuarios.forms import RegistrarTrabajadorForm, ModificarTrabajadorForm, AsignarCargoForm

from braces.views import LoginRequiredMixin

class RegistrarTrabajador(MensajeMixin, CreateView):
    model = Trabajador
    form_class = RegistrarTrabajadorForm
    success_url = reverse_lazy("usuarios:listado_trabajadores")
    template_name = "usuarios/trabajadores/registrar.html"
    mensaje_exito = "Trabajador registrado correctamente"
    mensaje_error = "Error al registrar el trabajador, por favor verificar los datos"

    def form_valid(self, form):
        elemento = form.save(commit=False)
        elemento.save()
        elemento.cargos.add(form.cleaned_data['cargos'])

        return redirect("usuarios:listado_trabajadores")

    def get_initial(self):
        initial = super().get_initial()
        initial['tipo_documento'] = TipoDocumento.obtener_tipo_cedula()
        return initial

class ModificarTrabajador(LoginRequiredMixin, UpdateView):
    model = Trabajador
    form_class = ModificarTrabajadorForm
    success_url = reverse_lazy("usuarios:listado_trabajadores")
    template_name = "usuarios/trabajadores/modificar.html"
    mensaje_exito = "Trabajador modificado correctamente"
    mensaje_error = "Error al modificar el trabajador, por favor verificar los datos"


class AsignarCargoTrabajador(LoginRequiredMixin, UpdateView):
    model = Trabajador
    form_class = AsignarCargoForm
    template_name = "usuarios/trabajadores/asignar_cargo.html"
    success_url = reverse_lazy("usuarios:listado_trabajadores")
    mensaje_exito = "Cargo asignado a trabajador correctamente"
    mensaje_error = "Error al asignar cargo al trabajador, por favor verificar los datos"

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

        return redirect("usuarios:listado_trabajadores")


class ListadoTrabajadores(ListView):
    model = Trabajador
    context_object_name = "trabajadores"
    template_name = "usuarios/trabajadores/listado.html"
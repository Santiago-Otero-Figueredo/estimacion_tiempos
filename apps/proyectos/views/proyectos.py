from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from ..models.proyectos import Proyecto
from ..models.contactos_proyecto import ContactoProyecto
from ..forms import (RegistrarProyectoForm,
                     ContactoFormSet)

from apps.utils.mixin import MensajeMixin



class RegistrarProyecto(MensajeMixin, CreateView):
    model = Proyecto
    form_class = RegistrarProyectoForm
    success_url = reverse_lazy("proyectos:listado_proyectos")
    template_name = "proyectos/proyectos/registrar.html"
    mensaje_exito = "Proyecto registrado correctamente"
    mensaje_error = "Error al registrar el proyecto, por favor verificar los datos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formset_estructuras = ContactoFormSet(queryset=ContactoProyecto.objects.none(), prefix="contacto")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = self.formset_estructuras
        return data

    def post(self, *args, **kwargs):

        formset = ContactoFormSet(self.request.POST, prefix="contacto")

        if formset.is_valid():
            self.form_valid(self.get_form())
            return self.formset_valid(formset)
        else:
            errores = ''
            for form in formset:
                for _, errors in form.errors.items():
                    errores += ('{}'.format(','.join(errors)))

            messages.error(self.request, "{}, {}".format(self.mensaje_error,errores))
            return redirect('estimaciones:registrar_proyecto')

    def formset_valid(self, formset):

        for form in formset:
            contacto = form.save(commit=False)
            contacto.proyecto = self.object
            contacto.save()
            
        return self.form_valid(self.get_form())

class ListadoProyecto(ListView):
    model = Proyecto
    context_object_name = "proyectos"
    template_name = "proyectos/proyectos/listado.html"
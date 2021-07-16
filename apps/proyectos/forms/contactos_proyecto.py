from django import forms
from django.forms import modelformset_factory

from ..models.contactos_proyecto import ContactoProyecto

class RegistrarContactoForm(forms.ModelForm):
    class Meta:
        model = ContactoProyecto
        fields = ("nombres", "apellidos", "correo_electronico", "phone_number", "cargo")

ContactoFormSet = modelformset_factory(ContactoProyecto, form=RegistrarContactoForm, extra=1)
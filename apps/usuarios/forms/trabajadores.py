from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.trabajadores import Trabajador
from apps.usuarios.models.tipos_cargos import TipoCargo

class RegistrarTrabajadorForm(UserCreationForm):

    cargos = forms.ModelChoiceField(queryset=TipoCargo.obtener_activos())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'].empty_label = None
        self.fields['cargos'].empty_label = None


    class Meta:
        model = Trabajador
        fields = ("tipo_documento", "numero_documento", "first_name", "last_name", "email", "phone_number", "cargos")

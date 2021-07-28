from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.usuarios.models.administradores import Administrador
from apps.usuarios.models.tipos_cargos import TipoCargo

class RegistrarAdministradorForm(UserCreationForm):

    cargos = forms.ModelChoiceField(queryset=TipoCargo.obtener_activos())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'].empty_label = None
        self.fields['cargos'].empty_label = None

    class Meta:
        model = Administrador
        fields = ("tipo_documento", "numero_documento", "first_name", "last_name", "email", "phone_number", "cargos")


class ModificarAdministradorForm(UserChangeForm):

    class Meta:
        model = Administrador
        fields = ("tipo_documento", "numero_documento", "first_name", "last_name", "email", "phone_number", "esta_activo")


class AsignarCargoForm(UserChangeForm):

    cargos = forms.ModelChoiceField(label="Cargo actual", queryset=TipoCargo.obtener_activos())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cargos'].empty_label = None

    class Meta:
        model = Administrador
        fields = ("cargos", )
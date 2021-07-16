from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.empresas import Empresa

class RegistrarEmpresaForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'].empty_label = None


    class Meta:
        model = Empresa
        fields = ("tipo_documento", "numero_documento", "first_name", "last_name", "email", "phone_number")

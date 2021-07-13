from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.empresas import Empresa

class RegistrarEmpresaForm(UserCreationForm):
    
    class Meta:
        model = Empresa
        fields = ("first_name", "last_name", "email", "phone_number")

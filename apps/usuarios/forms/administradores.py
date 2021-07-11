from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.administradores import Administrador

class RegistrarAdministradorForm(UserCreationForm):
    
    class Meta:
        model = Administrador
        fields = ("first_name", "last_name", "email", "phone_number")

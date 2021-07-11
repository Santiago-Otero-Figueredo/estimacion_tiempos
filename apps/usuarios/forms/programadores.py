from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.programadores import Programador

class RegistrarProgramadorForm(UserCreationForm):
    
    class Meta:
        model = Programador
        fields = ("first_name", "last_name", "email", "phone_number")

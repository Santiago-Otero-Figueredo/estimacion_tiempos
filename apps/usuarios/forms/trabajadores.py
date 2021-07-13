from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.trabajadores import Trabajador

class RegistrarTrabajadorForm(UserCreationForm):
    
    class Meta:
        model = Trabajador
        fields = ("first_name", "last_name", "email", "phone_number")

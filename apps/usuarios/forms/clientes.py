from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.usuarios.models.clientes import Cliente

class RegistrarClienteForm(UserCreationForm):
    
    class Meta:
        model = Cliente
        fields = ("first_name", "last_name", "email", "phone_number")

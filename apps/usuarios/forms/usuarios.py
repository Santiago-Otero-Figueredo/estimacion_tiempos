from django import forms

from apps.usuarios.models import Usuario
from django.contrib.auth.forms import AuthenticationForm


class FormularioInicioSesion(AuthenticationForm):
    username = forms.CharField(error_messages={
        'required': 'Este campo es requerido',
        'invalid': 'Introduzca un correo valido'
    })
    error_messages = {
        'invalid_login': (
            "Por favor introduzca un %(username)s valido y contraseña."
            "Los campos son sensibles a mayúsculas y minúsculas."
        ),
        'inactive': ("Esta cuenta esta inactiva"),
    }
    #password = forms.PasswordInput(label="Contraseña")

    def _init_(self, *args, **kwargs):
        print("Hey")
        super()._init_(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Correo electrónico'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['username'].label = ''
        self.fields['password'].label = ''

    class Meta:
        model = Usuario
        fields = ('username', 'password')
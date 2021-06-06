from django import forms

from apps.usuarios.models.programadores import Programador

class RegistrarProgramadorForm(forms.ModelForm):
    
    class Meta:
        model = Programador
        fields = ("email", "phone_number", "is_verified")

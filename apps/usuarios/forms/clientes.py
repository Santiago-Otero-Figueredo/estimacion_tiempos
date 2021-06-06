from django import forms

from apps.usuarios.models.clientes import Cliente

class RegistrarClienteForm(forms.ModelForm):
    
    class Meta:
        model = Cliente
        fields = ("email", "phone_number", "is_verified")

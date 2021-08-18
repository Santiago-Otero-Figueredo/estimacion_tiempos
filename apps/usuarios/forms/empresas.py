from django import forms

from apps.usuarios.models.empresas import Empresa

class RegistrarEmpresaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'].empty_label = None
        self.fields['first_name'].label = 'Nombre*'
        self.fields['tipo_documento'].label = 'Tipo de documento*'
        self.fields['numero_documento'].label = 'Número del documento*'


    class Meta:
        model = Empresa
        fields = ("tipo_documento", "numero_documento", "first_name", "email", "phone_number", "esta_activo")


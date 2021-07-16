from django import forms

from apps.usuarios.models.tipos_cargos import TipoCargo

class RegistrarCargoForm(forms.ModelForm):

    class Meta:
        model = TipoCargo
        fields = ("nombre", "descripcion")
        widgets = {
            'descripcion': forms.Textarea(
                attrs={
                    'rows': 4,
                    'cols': 22,
                    'style':'resize:none;'
                }
            )
        }

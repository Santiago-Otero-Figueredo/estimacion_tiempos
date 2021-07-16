from django import forms

from ..models.tipos_actividades import TipoActividad

class RegistrarTipoActividadForm(forms.ModelForm):
    
    class Meta:
        model = TipoActividad
        fields = ("nombre", "descripcion", "esta_activo")
        widgets = {
            'descripcion': forms.Textarea(
                attrs={
                    'rows': 4,
                    'cols': 22,
                    'style':'resize:none;'
                }
            )
        }
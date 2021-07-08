from django import forms

from apps.estimaciones.models.tipos_actividades import TipoActividad

class RegistrarTipoActividadForm(forms.ModelForm):
    
    class Meta:
        model = TipoActividad
        fields = ("nombre", "esta_activo")
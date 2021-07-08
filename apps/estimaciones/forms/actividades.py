from django import forms

from apps.estimaciones.models.actividades import Actividad

class RegistrarActividadForm(forms.ModelForm):
    
    class Meta:
        model = Actividad
        fields = ("tipo_actividad", "funcionalidad", "tiempo_estimado", "tiempo_real", "esta_activo")
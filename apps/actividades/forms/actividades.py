from django import forms

from ..models.actividades import Actividad

class RegistrarActividadForm(forms.ModelForm):
    
    class Meta:
        model = Actividad
        fields = ("tipo_actividad", "funcionalidad", "tiempo_estimado", "tiempo_real", "esta_activo")


class FiltroElementosJIRAForm(forms.Form):

    nombre_proyecto = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        proyectos = kwargs.pop('proyectos', tuple())
        super().__init__(*args, **kwargs)

        self.fields['nombre_proyecto'].empty_label = 'Todos'
        self.fields['nombre_proyecto'].choices = proyectos

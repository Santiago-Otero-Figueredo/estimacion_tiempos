from django import forms

from apps.usuarios.models.empleados import Empleado
from apps.proyectos.models.proyectos import Proyecto
from apps.actividades.models.actividades import TipoActividad

class FiltroEstimacionesForm(forms.Form):

    proyecto = forms.ModelChoiceField(label="Proyecto",queryset=Proyecto.obtener_activos(), required=False)
    empleado = forms.ModelChoiceField(label="Programador",queryset=Empleado.obtener_activos(), required=False)
    tipo_actividad = forms.ModelChoiceField(label="Tipo actividad",queryset=TipoActividad.obtener_activos(), required=False)
    
    fecha_inicio = forms.DateField(
                input_formats=['%Y-%m-%d'],
                widget=forms.TextInput(
                        attrs={
                            'class':'datepicker',
                            'placeholder': 'Fecha inicio',
                        }
                    ),
                label="", required=False)
    fecha_fin = forms.DateField(
                input_formats=['%Y-%m-%d'],
                widget=forms.TextInput(
                        attrs={
                            'class':'datepicker',
                            'placeholder': 'Fecha fin'
                        }
                    ),
                label="", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['proyecto'].empty_label = 'Todos'
        self.fields['empleado'].empty_label = 'Todos'
        self.fields['tipo_actividad'].empty_label = 'Todos'

from django import forms

from apps.usuarios.models.empleados import Empleado
from apps.actividades.models.estructuras import Estructura
from apps.proyectos.models.proyectos import Proyecto
from apps.actividades.models import TipoActividad

from django_select2.forms import ModelSelect2MultipleWidget

class FiltroEstimacionesForm(forms.Form):

    proyecto = forms.ModelChoiceField(label="Proyecto",queryset=Proyecto.obtener_activos(), required=False)
    empleado = forms.ModelChoiceField(label="Programador",queryset=Empleado.obtener_activos(), required=False)
    tipos_lugares = forms.ModelMultipleChoiceField(
                label="Actividades principales", 
                queryset=Estructura.obtener_actividades_lugar(),
                widget=ModelSelect2MultipleWidget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_lugar(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
                required=False
            )
    tipos_acciones = forms.ModelMultipleChoiceField(
                label="Tipos de acciones",
                queryset=Estructura.obtener_actividades_accion(),
                widget=ModelSelect2MultipleWidget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_accion(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
                required=False
            )
    tipos_tareas = forms.ModelMultipleChoiceField(
                label="Tipos de tareas",
                queryset=Estructura.obtener_actividades_tarea(),
                widget=ModelSelect2MultipleWidget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_tarea(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
                required=False
            )

    tipos_adicional = forms.ModelMultipleChoiceField(
                label="Tipos de actividades adicionales",
                queryset=Estructura.obtener_actividades_adicional(),
                widget=ModelSelect2MultipleWidget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_adicional(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
                required=False
            )

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
        self.fields['tipos_lugares'].empty_label = 'Todos'
        self.fields['tipos_acciones'].empty_label = 'Todos'
        self.fields['tipos_tareas'].empty_label = 'Todos'
        self.fields['tipos_adicional'].empty_label = 'Todos'

        
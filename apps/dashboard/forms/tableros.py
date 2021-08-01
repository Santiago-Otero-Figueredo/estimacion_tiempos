from apps.actividades.models.tipos_actividades import TipoActividad
from apps.actividades.models.estructuras import Estructura
from django import forms

from apps.usuarios.models.empleados import Empleado
from apps.proyectos.models.proyectos import Proyecto

from django_select2.forms import ModelSelect2MultipleWidget

class FiltroTablerosForm(forms.Form):

    proyecto = forms.ModelMultipleChoiceField(
        label="Proyecto",
        queryset=Proyecto.obtener_todos(),
        required=False,
        widget=ModelSelect2MultipleWidget(
                model=Proyecto,
                queryset=Proyecto.obtener_todos(),
                search_fields=['nombre__icontains'],
                max_results=100,
                attrs={
                    'data-minimum-input-length':0
                }
            ),
    )
    empleado = forms.ModelChoiceField(label="Programador",queryset=Empleado.obtener_activos(), required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['proyecto'].empty_label = 'Todos'
        self.fields['empleado'].empty_label = 'Todos'


class FiltroEstimacionesTiemposForm(forms.Form):

    proyecto = forms.ModelMultipleChoiceField(
        label="Proyecto",
        queryset=Proyecto.obtener_todos(),
        required=False,
        widget=ModelSelect2MultipleWidget(
                model=Proyecto,
                queryset=Proyecto.obtener_todos(),
                search_fields=['nombre__icontains'],
                max_results=100,
                attrs={
                    'data-minimum-input-length':0
                }
            ),
    )
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['proyecto'].empty_label = 'Todos'
        self.fields['empleado'].empty_label = 'Todos'
        self.fields['tipos_lugares'].empty_label = 'Todos'
        self.fields['tipos_acciones'].empty_label = 'Todos'
        self.fields['tipos_tareas'].empty_label = 'Todos'

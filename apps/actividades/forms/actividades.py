from django import forms
from django.forms import modelformset_factory

from django_select2.forms import ModelSelect2Widget

from ..models.estructuras import Estructura
from ..models.actividades import Actividad
from ..models.tipos_actividades import TipoActividad



class RegistrarActividadForm(forms.ModelForm):

    tipos_lugares = forms.ModelChoiceField(
                label="Tipos actividades lugares",
                queryset=Estructura.obtener_actividades_lugar(),
                widget=ModelSelect2Widget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_lugar(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
            )
    tipos_acciones = forms.ModelChoiceField(
                label="Tipos actividades acciones",
                queryset=Estructura.obtener_actividades_accion(),
                widget=ModelSelect2Widget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_accion(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
            )
    tipos_tareas = forms.ModelChoiceField(
                label="Tipos actividades tareas",
                queryset=Estructura.obtener_actividades_tarea(),
                widget=ModelSelect2Widget(
                    model=TipoActividad,
                    queryset=Estructura.obtener_actividades_tarea(),
                    search_fields=['nombre__icontains'],
                    max_results=100,
                    attrs={
                        'data-minimum-input-length':0
                    }
                ),
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tipos_lugares'].empty_label = 'Ninguno'
        self.fields['tipos_acciones'].empty_label = 'Ninguno'
        self.fields['tipos_tareas'].empty_label = 'Ninguno'
    class Meta:
        model = Actividad
        fields = ("tipos_lugares" ,"tipos_acciones" ,"tipos_tareas" ,
                    "funcionalidad", "tiempo_estimado", "tiempo_real", "esta_activo")


class FiltroElementosJIRAForm(forms.Form):

    nombre_proyecto = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        proyectos = kwargs.pop('proyectos', tuple())
        super().__init__(*args, **kwargs)

        self.fields['nombre_proyecto'].empty_label = 'Todos'
        self.fields['nombre_proyecto'].choices = proyectos


class AsignarActividadForm(forms.ModelForm):

    tipos_lugares = forms.ModelChoiceField(
                label="Tipos actividades lugares",
                queryset=Estructura.obtener_actividades_lugar(),
                required=False
            )
    tipos_acciones = forms.ModelChoiceField(
                label="Tipos actividades acciones",
                queryset=Estructura.obtener_actividades_accion(),
                required=False
            )
    tipos_tareas = forms.ModelChoiceField(
                label="Tipos actividades tareas",
                queryset=Estructura.obtener_actividades_tarea(),
                required=False
            )

    identificador = forms.CharField(required=False)
    funcionalidad = forms.CharField(widget=forms.Textarea(
                attrs={'rows': 4,
                    'cols': 40,
                    'style': 'height: auto;'}
                ),
                required=False
            )

    registrar = forms.BooleanField(
        label="",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipos_lugares'].empty_label = 'Ninguno'
        self.fields['tipos_acciones'].empty_label = 'Ninguno'
        self.fields['tipos_tareas'].empty_label = 'Ninguno'

        tipos = list(Actividad.obtener_actividades_similares(self.instance.funcionalidad))

        if tipos and len(tipos) >= 3:
            self.fields['tipos_lugares'].initial = tipos[0]
            self.fields['tipos_acciones'].initial = tipos[1]
            self.fields['tipos_tareas'].initial = tipos[2]
            self.fields['registrar'].initial = True

    class Meta:
        model = Actividad
        fields = ("identificador", "tipos_lugares", "tipos_acciones",
                    "tipos_tareas",  "funcionalidad", "registrar")

AsignarActividadFormSet = modelformset_factory(Actividad, form=AsignarActividadForm, extra=0)

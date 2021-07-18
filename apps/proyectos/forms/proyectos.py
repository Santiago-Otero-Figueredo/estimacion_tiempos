from django import forms

from ..models.proyectos import Proyecto


class RegistrarProyectoForm(forms.ModelForm):
    
    fecha_inicio = forms.DateTimeField(
                input_formats=['%Y-%m-%d'],
                widget=forms.TextInput(
                        attrs={
                            'class':'datepicker',
                            'placeholder': 'Fecha inicio',
                        }
                    ),
                label="", required=False)
    fecha_finalizacion = forms.DateTimeField(
                input_formats=['%Y-%m-%d'],
                widget=forms.TextInput(
                        attrs={
                            'class':'datepicker',
                            'placeholder': 'Fecha fin'
                        }
                    ),
                label="", required=False)
    class Meta:
        model = Proyecto
        fields = ("empresa", "nombre", "identificador_jira", "descripcion", "fecha_inicio", "fecha_finalizacion", "esta_activo")
        widgets = {
            'descripcion': forms.Textarea(
                attrs={
                    'rows': 7,
                    'cols': 22,
                    'style':'resize:none;'
                }
            )
        }

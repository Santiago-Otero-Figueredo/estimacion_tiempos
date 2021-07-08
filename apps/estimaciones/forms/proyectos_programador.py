from django import forms

from apps.estimaciones.models.proyecto_programador import ProyectoProgramador

class RegistrarProyectoProgramadorForm(forms.ModelForm):
    
    class Meta:
        model = ProyectoProgramador
        fields = ("programador", "proyecto", "esta_activo")
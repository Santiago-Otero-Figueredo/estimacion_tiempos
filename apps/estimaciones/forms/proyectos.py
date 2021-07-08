from django import forms

from apps.estimaciones.models.proyectos import Proyecto

class RegistrarProyectoForm(forms.ModelForm):
    
    class Meta:
        model = Proyecto
        fields = ("cliente", "nombre", "esta_activo")
    
   
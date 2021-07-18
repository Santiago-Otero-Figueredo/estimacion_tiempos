from django import forms

from ..models.proyectos_empleados import ProyectoEmpleado

class RegistrarProyectoEmpleadoForm(forms.ModelForm):
    
    class Meta:
        model = ProyectoEmpleado
        fields = ("empleado", "proyecto")
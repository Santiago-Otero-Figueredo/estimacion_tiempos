from django import forms

from apps.estimaciones.models.proyectos_empleados import ProyectoEmpleado

class RegistrarProyectoEmpleadoForm(forms.ModelForm):
    
    class Meta:
        model = ProyectoEmpleado
        fields = ("empleado", "proyecto", "esta_activo")
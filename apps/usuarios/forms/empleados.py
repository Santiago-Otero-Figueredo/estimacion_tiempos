from django import forms
from django.forms import models

from ..models.empleados import Empleado

class ModificarEmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = ("tipo_usuario", "tipo_documento", "numero_documento", "first_name", "last_name", "email", "phone_number", "esta_activo")

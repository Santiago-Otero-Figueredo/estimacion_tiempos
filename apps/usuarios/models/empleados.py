from apps.usuarios.models.tipos_cargo_empelado import CargoEmpleado
from django.db import models

from apps.usuarios.models.tipos_cargos import TipoCargo
from apps.usuarios.models.usuarios import Usuario

class Empleado(Usuario):
    cargos = models.ManyToManyField(
        TipoCargo,
        through='CargoEmpleado',
        related_name="empleados_cargos",
        blank=True,
        verbose_name="Cargos asociados al empleado"
    )

    
    def obtener_cargos(self):
        return self.empleados_cargos

    def obtener_ultimo_cargo(self):
        cargo = self.cargos.order_by('-creado').first()
        if cargo:
            return cargo.nombre
        else:
            return None






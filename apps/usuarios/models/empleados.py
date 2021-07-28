from apps.usuarios.models.tipos_cargo_empelado import CargoEmpleado
from django.db import models

from apps.usuarios.models.tipos_cargos import TipoCargo
from apps.usuarios.models.usuarios import Usuario

class Empleado(Usuario):
    identificador_jira = models.CharField(max_length=80, verbose_name="Identificador único de JIRA", default='')
    cargos = models.ManyToManyField(
        TipoCargo,
        through='CargoEmpleado',
        related_name="empleados_cargos",
        blank=True,
        verbose_name="Cargos asociados al empleado"
    )

    @classmethod
    def obtener_identificadores(cls) -> 'list<str>':
        return list(cls.objects.values_list('identificador_jira', flat=True))
    
    @staticmethod
    def obtener_empleados_sin_tipo() -> 'Queryset<Empleado>':
        return Empleado.objects.filter(tipo_usuario__isnull=True)

    def obtener_cargos(self):
        return self.empleados_cargos

    def obtener_ultimo_cargo(self):
        cargo = self.cargos.order_by('-cargos_empleado_proyecto__fecha_cambio_cargo').first()
        if cargo:
            return cargo
        return None

    def obtener_cargos_por_orden_ascendente(self):
        return self.cargos.order_by('-cargos_empleado_proyecto__fecha_cambio_cargo').values(
            'nombre',
            'cargos_empleado_proyecto__fecha_cambio_cargo',
            'cargos_empleado_proyecto__fecha_asignado'
            )






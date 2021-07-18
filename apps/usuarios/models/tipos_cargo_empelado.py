from django.db import models
from django.utils import timezone

from apps.utils.models import EstimacionModel


class CargoEmpleado(EstimacionModel):
    empleado = models.ForeignKey(
        'Empleado',
        related_name='cargos_empleado_empleado',
        verbose_name="Empleado",
        on_delete=models.PROTECT
    )
    cargo = models.ForeignKey(
        'TipoCargo',
        related_name='cargos_empleado_proyecto',
        verbose_name="Proyecto",
        on_delete=models.PROTECT
    )
    fecha_asignado = models.DateTimeField(
        'Asignado a',
        auto_now_add=True,
        help_text='Fecha y hora en la que se asigno el cargo al trabajador'
    )
    fecha_cambio_cargo = models.DateTimeField(
        'Cambio de cargo a',
        auto_now=True,
        help_text='Fecha y hora en la que se realizo un cambio de cargo al trabajador'
    )

    def save(self, *args, **kwargs):
        self.fecha_cambio_cargo = timezone.now()
        return super().save(*args, **kwargs)

    @staticmethod
    def crear_y_obtener(empleado:'Empleado', cargo:'TipoCargo') -> 'TipoActividad':

        if CargoEmpleado.existe(empleado, cargo):
            return CargoEmpleado.buscar_por_empleado_y_cargo(empleado, cargo)
        else:
            CargoEmpleado.objects.create(empleado=empleado, cargo=cargo)

    @staticmethod
    def existe(empleado:'Empleado', cargo:'TipoCargo') -> bool:
        try:
            CargoEmpleado.objects.get(empleado=empleado, cargo=cargo)
            return True
        except CargoEmpleado.DoesNotExist:
            return False

    @staticmethod
    def buscar_por_empleado_y_cargo(empleado:'Empleado', cargo:'TipoCargo') -> "CargoEmpleado":
        try:
            return CargoEmpleado.objects.get(empleado=empleado, cargo=cargo)
        except CargoEmpleado.DoesNotExist:
            return CargoEmpleado.objects.none()

    @staticmethod
    def buscar_por_empleado(empleado:'Empleado') -> "Queryset<CargoEmpleado>":
        return CargoEmpleado.objects.filter(empleado=empleado)

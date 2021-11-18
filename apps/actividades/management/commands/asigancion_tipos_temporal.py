
from django.core.management.base import BaseCommand
from django.db.models import Count, Q


from ...models.actividades import Actividad
from ...models.tipos_actividades import TipoActividad
from ...models.caminos_actividades import CaminoActividad

from apps.proyectos.models.proyectos import Proyecto
from apps.proyectos.models.proyectos_empleados import ProyectoEmpleado

from apps.usuarios.models.empleados import Empleado
from apps.utils.clases.jira.ConexionJira import Jira

import unicodedata
import re

class Command(BaseCommand):
    help = 'Carga los datos iniciales de las historias de usuario desde un archivo Excel'

    def handle(self, *args, **kwargs):


        
    
        try:
            actividades = Actividad.objects.filter(
                Q(slug_tipos__isnull=True) |
                Q(slug_tipos__exact='')
                )
            
            for actividad in actividades:
                nombre_actividad = actividad.funcionalidad
                
                actividades_similares = Actividad.objects.exclude(slug_tipos__isnull=True).exclude(slug_tipos__exact='').filter(
                    Q(funcionalidad__icontains=nombre_actividad) |
                    Q(funcionalidad__trigram_similar=nombre_actividad) |
                    Q(slug_tipos__icontains=nombre_actividad) |
                    Q(tipos_actividades__nombre__icontains=nombre_actividad)
                ).values(
                    'slug_tipos'
                ).annotate(total=Count('slug_tipos')).order_by('-total').values('pk', 'slug_tipos', 'total').first()
                
                if actividades_similares:
                    actividad_mayor_similitud = Actividad.objects.get(pk=actividades_similares['pk'])

        except Exception as e:
            print("Errro", e)


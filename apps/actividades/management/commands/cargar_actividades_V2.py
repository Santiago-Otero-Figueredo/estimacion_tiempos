
from django.core.management.base import BaseCommand

from apps.utils.clases.pandas import GestorLectorArchivo

from ...models.actividades import Actividad
from ...models.tipos_actividades import TipoActividad
from ...models.caminos_actividades import CaminoActividad
from ...utils import crear_slug_tipos_actividad

from apps.proyectos.models.proyectos import Proyecto
from apps.proyectos.models.proyectos_empleados import ProyectoEmpleado

from apps.usuarios.models.empleados import Empleado


class Command(BaseCommand):
    help = 'Carga los datos iniciales de las historias de usuario desde un archivo Excel'

    def handle(self, *args, **kwargs):

        gestor = GestorLectorArchivo("F:\\santiago\\Datos Personales\\Documentos pasantia\\proyecto\\estimacion_tiempos\\_data\\jira_actividades.xlsx")

        data_frame = gestor.obtener_dataframe().fillna(0)

        for index, row in data_frame.iterrows():
            try:
                tipo_actividad_1 = TipoActividad.buscar_por_nombre(row['Tipo_uno'])
                tipo_actividad_2 = TipoActividad.buscar_por_nombre(row['Tipo_dos'])
                tipo_actividad_3 = TipoActividad.buscar_por_nombre(row['Tipo_tres'])
                proyecto = Proyecto.buscar_por_nombre(row['Proyecto'].capitalize())
                empleado = Empleado.buscar_por_nombre_y_apellido(row['Assignee'].strip()).first()
           
                if empleado:
                    proyecto_empleado = ProyectoEmpleado.crear_y_obtener(empleado, proyecto)
                    key_historia = str(row['Issue key'])
                    funcionalidad = str(row['Descripcion'])

                    tiempo_estimado = float(row['Original estimate']/60)
                    tiempo_real = float(row['Time Spent']/60)

                    actividad_adicional = None
                    if 'adicional' in funcionalidad.lower().strip():
                        if  TipoActividad.existe_por_nombre('Adicional') == True:
                            actividad_adicional = TipoActividad.buscar_por_nombre('Adicional')
                        else:
                            actividad_adicional = TipoActividad.objects.create(nombre='Adicional')

                    tipo_adicional = None
                    if not actividad_adicional is None:
                        tipo_adicional = actividad_adicional.nombre
                   
                    slug_tipos = crear_slug_tipos_actividad(
                        tipo_actividad_1.nombre,
                        tipo_actividad_2.nombre,
                        tipo_actividad_3.nombre,
                        tipo_adicional
                    )
                   
                    actividad = Actividad.objects.create(
                        identificador=key_historia,
                        proyecto_empleado=proyecto_empleado,
                        funcionalidad=funcionalidad,
                        tiempo_estimado=tiempo_estimado,
                        tiempo_real=tiempo_real,
                        slug_tipos=slug_tipos
                    )
                   
                    actividad.tipos_actividades.add(tipo_actividad_1)
                    actividad.tipos_actividades.add(tipo_actividad_2)
                    actividad.tipos_actividades.add(tipo_actividad_3)

                    if not actividad_adicional is None:
                        actividad.tipos_actividades.add(actividad_adicional)

                    actividad.save()

                else:
                    print("Programador inexistente")
                
            except Exception as e:
                print("Errro", e)
        

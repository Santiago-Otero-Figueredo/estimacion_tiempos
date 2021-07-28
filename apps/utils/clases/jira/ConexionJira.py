from apps.proyectos.models.proyectos_empleados import ProyectoEmpleado
from apps.proyectos.models.proyectos import Proyecto
from apps.actividades.models.actividades import Actividad
from requests.auth import HTTPBasicAuth

from apps.usuarios.models.empleados import Empleado

import requests
import json



class JiraException(Exception):
    pass

class Jira:
    

    def __init__(self) -> None:
        self.__url = "https://danalytics.atlassian.net/"
        self.__usuario = 'andres.c.serna@gmail.com'
        self.__token = '9YpfaX22NIqiFNaFQ27U4501'
        self.__autenticacion = HTTPBasicAuth(self.__usuario, self.__token)
        self.__headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
    
    def registrar_historia_usuario(self):

        url = '{}/rest/api/2/issue'.format(self.__url)

        payload = json.dumps( {
            "fields": {
                "project": {
                    "key": "EDT"
                },
                "summary": "Prueba clase",
                "description": "Order entry fails when selecting supplier.",
                "issuetype":{
                    "name":"Story"
                }
            }
        } )
        self.enviar_peticion_post('POST', url, payload)


    def consultar_todos_los_usuarios(self) -> 'list<dict>':

        url = '{}/rest/api/3/users/search'.format(self.__url)
        
        lista_usuarios = list()
        query = {}
        response = self.enviar_peticion_get(url, query)
        data = response.json()
        identificadores_registrados = Empleado.obtener_identificadores()
        for usuario in data:
            if usuario['accountType'] == 'atlassian' and not usuario['accountId'] in identificadores_registrados:
                lista_usuarios.append(usuario)

        return lista_usuarios


    def consultar_todos_los_proyectos(self) -> 'list<dict>':

        url = '{}/rest/api/3/project/'.format(self.__url)
        
        lista_proyectos = list()
        query = {}
        response = self.enviar_peticion_get(url, query)
        data = response.json()
        for proyecto in data:
            lista_proyectos.append(
                {
                    'key':proyecto['key'],
                    'nombre':proyecto['name']
                }
            )

        return lista_proyectos

    def consultar_historias_usuarios(self, proyecto:str) -> 'list<dict>':

        url = '{}/rest/api/3/search/'.format(self.__url)
        existen_elementos = True
        lista_historias_consultadas = list()
        
        identificadores_registrados_jira = Actividad.obtener_todos().values_list('identificador', flat=True)

        if proyecto:
            inicio = 0
            maximo = 100
            while(existen_elementos):
                query = {
                    'jql': 'project = {} AND status=Done AND originalEstimate is not EMPTY AND timespent>0'.format(proyecto),
                    'startAt':inicio,
                    'maxResults':maximo
                }

                response = self.enviar_peticion_get(url, query)

                data = response.json()
                hisorias = data['issues']
                if len(hisorias) == 0:
                    existen_elementos = False
                    break

                for historia in hisorias:
                    key = historia['key']
                    if not key in identificadores_registrados_jira:
                        campos = historia['fields']
                        tiempo_total = campos['aggregatetimespent']
                        tiempo_estimado = campos['aggregatetimeoriginalestimate']
                        if tiempo_total == 0 or tiempo_estimado == 0:
                            continue
                        fecha_creacion = campos['created']
                        if campos['customfield_10020'] is None or not 'endDate' in campos['customfield_10020'][0]:
                            continue
                        fecha_inicio = campos['customfield_10020'][0].pop('startDate', fecha_creacion)
                        fecha_finalizacion = campos['customfield_10020'][0]['endDate']
                        nombre_actividad = campos['summary']
                        nombre_usuario_asignado = 'Sin asignar'
                        if campos['assignee']:
                            if 'displayName' in campos['assignee'].keys():
                                nombre_usuario_asignado = campos['assignee']['displayName']
                        lista_historias_consultadas.append(
                            {
                                'key':key,
                                'nombre_actividad':nombre_actividad,
                                'tiempo_total':float(tiempo_total/60),
                                'tiempo_estimado':float(tiempo_estimado/60),
                                'nombre_usuario_asignado':nombre_usuario_asignado,
                                'fecha_creacion':fecha_creacion,
                                'fecha_inicio':fecha_inicio,
                                'fecha_finalizacion':fecha_finalizacion,
                            }
                        )
                    
                inicio = maximo
                maximo += 100
        return lista_historias_consultadas


    def cargar_actividades_de_proyecto(self, proyecto:str):

        historias_usuario = self.consultar_historias_usuarios(proyecto)
        for historia_usuario in historias_usuario:
            try:
                proyecto_registrado = Proyecto.buscar_por_identificador_jira(proyecto)
                empleado = Empleado.buscar_por_nombre_y_apellido(historia_usuario['nombre_usuario_asignado'].strip()).first()
                actividad = Actividad.obtener_por_identificador_jira(historia_usuario['key'])
                if empleado and actividad.count() == 0:
                    proyecto_empleado = ProyectoEmpleado.crear_y_obtener(empleado, proyecto_registrado)
                    key_historia = str(historia_usuario['key'])
                    print(historia_usuario)
                    funcionalidad = historia_usuario['nombre_actividad']

                    actividad = Actividad.objects.create(
                            identificador=key_historia,
                            proyecto_empleado=proyecto_empleado,
                            funcionalidad=funcionalidad,
                            tiempo_estimado=historia_usuario['tiempo_estimado'],
                            tiempo_real=historia_usuario['tiempo_total'],
                            slug_tipos=''
                        )
            except Exception as e:
                print("Errro", e)
           


    def enviar_peticion_post(self, url, payload):
        response = requests.request(
            'POST',
            url,
            data=payload,
            headers=self.__headers,
            auth=self.__autenticacion
        )
        #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return response

    def enviar_peticion_get(self, url, params):
        response = requests.request(
            'GET',
            url,
            params=params,
            headers=self.__headers,
            auth=self.__autenticacion
        )
        #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return response
        

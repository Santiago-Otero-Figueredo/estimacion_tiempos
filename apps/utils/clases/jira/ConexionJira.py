from requests.auth import HTTPBasicAuth

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
        if proyecto:
            inicio = 0
            maximo = 100
            while(existen_elementos):
                query = {
                    'jql': 'project = {}'.format(proyecto),
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
                    
                    campos = historia['fields']
                    tiempo_total = campos['aggregatetimespent']
                    if tiempo_total is None:
                        continue
                    
                    tiempo_estimado = campos['aggregatetimeoriginalestimate']
                    if tiempo_estimado is None:
                        continue
                    if key == 'PRIAL-440':
                        
                        print(tiempo_total, tiempo_estimado)
                        print(campos)

                    fecha_creacion = campos['created']

                    if campos['customfield_10020']:
                        if 'startDate' in campos['customfield_10020'][0] and 'startDate' in campos['customfield_10020'][0]:
                            fecha_inicio = campos['customfield_10020'][0]['startDate']
                            fecha_finalizacion = campos['customfield_10020'][0]['startDate']
                        else:
                            continue
                    else:
                        fecha_inicio = ''
                        fecha_finalizacion = ''

                    if campos['assignee']:
                        if 'emailAddress' in campos['assignee'].keys():
                            correo_usuario_asignado = campos['assignee']['emailAddress']
                        else:
                            correo_usuario_asignado = ""
                        nombre_usuario_asignado = campos['assignee']['displayName']
                    else:
                        correo_usuario_asignado = ''
                        nombre_usuario_asignado = ''
                    if campos['status']:
                        estado = campos['status']['name']
                    else:                
                        estado = ''

                    nombre_actividad = campos['summary']
                    
                    lista_historias_consultadas.append(
                        {
                            'key':key,
                            'nombre_actividad':nombre_actividad,
                            'tiempo_total':float(tiempo_total/60),
                            'tiempo_estimado':float(tiempo_estimado/60),
                            'correo_usuario_asignado':correo_usuario_asignado,
                            'nombre_usuario_asignado':nombre_usuario_asignado,
                            'fecha_creacion':fecha_creacion,
                            'fecha_inicio':fecha_inicio,
                            'fecha_finalizacion':fecha_finalizacion,
                            'estado':estado
                        }
                    )
                    #print(key, nombre_actividad)
                inicio = maximo
                maximo += 100
                print("### length: ", len(lista_historias_consultadas))
        return lista_historias_consultadas


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
        

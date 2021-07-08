from config.settings.base import DIRECCION_HOST
import requests

def enviar_peticion_rest_no_sql(url_peticion, parametros):
    url = "{}{}".format(DIRECCION_HOST, url_peticion)
    respuesta_peticion = requests.get(url, json=parametros)
    if respuesta_peticion.ok:
        return respuesta_peticion.json()

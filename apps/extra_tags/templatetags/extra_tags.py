from django import template

register = template.Library()

@register.simple_tag(name='convertir_elementos_a_lista')
def convertir_elementos_a_lista(*args) -> 'list<dict>':
    """
        Convierte una listad e strings en una lista de diccionarios

        Retorna:
            list<dict>: Lista de diccionarios agrupados
    """
    lista_opciones = []
    if len(args) > 2:
        for index in range(0, int(len(args)/2)+2, 2):
            lista_opciones.append({'url':args[index], 'nombre':args[index + 1]})
    else:
        lista_opciones.append({'url':args[0], 'nombre':args[1]})
    return lista_opciones

@register.simple_tag(name='obtener_icono')
def obtener_icono(nombre_opcion) -> str:
    icono = ''

    if 'Modificar' in nombre_opcion:
        icono = 'fas fa-edit'
    elif 'Consultar' in nombre_opcion:
        icono = 'fas fa-eye'
    elif 'Propio' in nombre_opcion or 'propio' in nombre_opcion:
        icono = 'fas fa-shopping-cart'
    elif 'Competencia' in nombre_opcion or 'competencia' in nombre_opcion:
        icono = 'fas fa-balance-scale'
    elif 'Canales' in nombre_opcion:
        icono = 'fas fa-truck'
    elif 'Marcar como leída' in nombre_opcion:
        icono = 'far fa-envelope-open'
    elif 'Marcar como no leída' in nombre_opcion:
        icono = 'far fa-envelope'
    elif 'Registrar' in nombre_opcion:
        icono = 'fas fa-plus'
    elif 'Adquirir' in nombre_opcion:
        icono = 'fas fa-shopping-cart'
    elif 'Agregar' in nombre_opcion:
        icono = 'fas fa-plus-circle'
    else:
        icono = 'fas fa-angle-double-right'

    return icono


@register.filter(name='split')
def split(value):
    return value.split(' ')
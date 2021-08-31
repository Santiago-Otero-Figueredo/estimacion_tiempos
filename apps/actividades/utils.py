
def crear_slug_tipos_actividad(tipo_act_1, tipo_act_2, tipo_act_3, tipo_act_4:str=None):
    """ Crea los slug_name usando las actividades que recibe como parámetros"""

    slug_tipos = '{}-{}-{}'.format(
                        tipo_act_1.capitalize(),
                        tipo_act_2.capitalize(),
                        tipo_act_3.capitalize()
                    )
    if not tipo_act_4 is None:
        slug_tipos += '-' + tipo_act_4

    return slug_tipos

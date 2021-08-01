
def crear_slug_tipos_actividad(tipo_actividad_1, tipo_actividad_2, tipo_actividad_3, tipo_actividad_4:str=None):

    slug_tipos = '{}-{}-{}'.format(
                        tipo_actividad_1.capitalize(),
                        tipo_actividad_2.capitalize(),
                        tipo_actividad_3.capitalize()
                    )
    if not tipo_actividad_4 is None:
        slug_tipos += '-' + tipo_actividad_4

    return slug_tipos
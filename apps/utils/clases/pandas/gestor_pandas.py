from abc import ABCMeta

import pandas as pd


class GestorLectorArchivo(metaclass=ABCMeta):
    _isumo_datos = None
    _dataframe = None

    def __init__(self, isumo_datos, *args, **kwargs):
        self._isumo_datos = isumo_datos

    def obtener_dataframe(self) -> 'Dataframe':
        return self._dataframe


class GestorLectorQueryset(GestorLectorArchivo):
      
    def __init__(self, isumo_datos, *args, **kwargs):
        super().__init__(isumo_datos=isumo_datos)
       
        self.obtener_dataframe_de_queryset()
    
    def obtener_dataframe_de_queryset(self) -> 'Dataframe':
        """
            Retorna un dataframe usando un archivo de excel como parámetro

            Parámetros:
                archivo: archivo de excel que contiene la información 

            Retorno:
                Dataframe: dataframe
        """
        self._dataframe = pd.DataFrame(self._isumo_datos)


def obtener_valores_sin_repetir_columna(data_frame:'DataFarme', columna:str) -> 'list<str>':
    """Retorna los valores sin repetir de la columna del dataframe"""
    return data_frame[columna].unique().tolist()

def eliminar_ceros(data_frame:'DataFarme'):
    """Elimina todos las filas que posean un cero en sus registros"""
    df = data_frame[(data_frame != 0).all(1)]
    return df

def obtener_rangos_atipicos(data_frame:'DataFarme', columna:str):
    """Retorna los rangos atípicos de la columna seleccionada del dataframe recibido como parámetro"""
    q1, q3, iqr = 0, 0, 0
    if columna in data_frame.columns:
        q1 = data_frame[columna].quantile(0.25) 
        q3 = data_frame[columna].quantile(0.75)
        iqr = q3-q1 #Rango intercuartil
    minimo  = q1-1.5*iqr 
    maximo = q3+1.5*iqr
    return (minimo, maximo)

def eliminar_valores_atipicos(data_frame:'DataFarme', columna:str):
    """Retorna el el dataframe recibido como parámetro sin los valores atípicos de la columna recibida como paramtero"""
    if columna in data_frame.columns:
        minimo, maximo = obtener_rangos_atipicos(data_frame, columna)
        df = data_frame.loc[(data_frame[columna] > minimo) & (data_frame[columna] < maximo)]
        return df
    else:
        return pd.DataFrame()

def obtener_valores_atipicos(data_frame:'DataFarme', columna:str):
    minimo, maximo = obtener_rangos_atipicos(data_frame, columna)
    df = data_frame.loc[(data_frame[columna] <= minimo) | (data_frame[columna] >= maximo)]
    return df

def obtener_describe_dataframe(data_frame:'DataFarme', columnas_agrupacion:'list<str>', columna_informacion):
    diccionario_de_estimaciones = dict()
    if not data_frame.empty:
        data_frame = data_frame.groupby(columnas_agrupacion)[columna_informacion].describe()
        for index, row in data_frame.iterrows():
            row = row.fillna(0)
            diccionario_de_estimaciones[index] = {
                    'nombre':index,
                    'cantidad':row['count'],
                    'promedio':row['mean'],
                    'minimo':row['min'],
                    'maximo':row['max'],
                    'desviacion':row['std']
                }

    return diccionario_de_estimaciones
from abc import ABCMeta

import pandas as pd


class GestorLectorArchivo(metaclass=ABCMeta):
    _isumo_datos = None
    _dataframe = None

    def __init__(self, isumo_datos, *args, **kwargs):
        self._isumo_datos = isumo_datos

    def obtener_dataframe(self) -> 'Dataframe':
        return self._dataframe

class GestorLectorExcel(GestorLectorArchivo):

    def __init__(self, isumo_datos, *args, **kwargs):
        super().__init__(isumo_datos=isumo_datos)
       
        self.obtener_dataframe_de_excel()

    def obtener_dataframe_de_excel(self) -> 'Dataframe':
        """
            Retorna un Dataframe usando un archivo de excel como parámetro

            Parámetros:
                archivo: archivo de excel que contiene la información 

            Retorno:
                Dataframe: Dataframe
        """

        self._dataframe = pd.read_excel(self._isumo_datos, engine='openpyxl')        
        cols = self._dataframe.columns[~self._dataframe.columns.str.startswith('Unnamed:')]
        self._dataframe = self._dataframe[cols].dropna(how='all')


class GestorLectorQueryset(GestorLectorArchivo):
      
    def __init__(self, isumo_datos, *args, **kwargs):
        super().__init__(isumo_datos=isumo_datos)
       
        self.obtener_dataframe_de_queryset()
    
    def obtener_dataframe_de_queryset(self) -> 'Dataframe':
        """
            Retorna un Dataframe usando un archivo de excel como parámetro

            Parámetros:
                archivo: archivo de excel que contiene la información 

            Retorno:
                Dataframe: Dataframe
        """
        self._dataframe = pd.DataFrame(self._isumo_datos)

def obtener_data_frame_por_valor_en_columna(data_frame:'DataFrame', columna_buscar:str, valor_buscar:str) -> 'DataFrame':
    """
    Retorna un DataFrame filtrando los registros con columna y valor recibidos como parametro

    Parámetros:
        data_frame (DataFrame): DataFrame que contiene la información
        columna_buscar (str): Columna donde se realizara el filtro
        valor_buscar (str): valor que se buscara en la columna

    Retorno:
        DataFrame: Con los registros que cumplan con el filtrado
    """
    data_frame_filtrado = data_frame.loc[data_frame[columna_buscar] == valor_buscar]
    return data_frame_filtrado

def obtener_valores_sin_repetir_columna(data_frame:'DataFarme', columna:str) -> 'list<str>':
    """Retorna los valores sin repetir de la columna del DataFrame"""
    return data_frame[columna].unique().tolist()

def eliminar_ceros(data_frame:'DataFarme') -> 'DataFarme':
    """Elimina todos las filas que posean un cero en sus registros"""
    df = data_frame[(data_frame != 0).all(1)]
    return df

def obtener_rangos_atipicos(data_frame:'DataFarme', columna:str) -> tuple:
    """Retorna los rangos atípicos de la columna seleccionada del DataFrame recibido como parámetro"""
    q1, q3, iqr = 0, 0, 0
    if columna in data_frame.columns:
        q1 = data_frame[columna].quantile(0.25) 
        q3 = data_frame[columna].quantile(0.75)
        iqr = q3-q1 #Rango intercuartil
    minimo  = q1-1.5*iqr 
    maximo = q3+1.5*iqr
    return (minimo, maximo)

def eliminar_valores_atipicos(data_frame:'DataFarme', columna:str) -> 'DataFarme':
    """Retorna el DataFrame recibido como parámetro sin los valores atípicos de la columna recibida como parámetro"""
    if columna in data_frame.columns:
        minimo, maximo = obtener_rangos_atipicos(data_frame, columna)
        df = data_frame.loc[(data_frame[columna] > minimo) & (data_frame[columna] < maximo)]
        return df
    else:
        return pd.DataFrame()

def obtener_valores_atipicos(data_frame:'DataFarme', columna:str) -> 'DataFarme':
    """Retorna el DataFrame recibido como parámetro con los valores atípicos de la columna recibida como parámetro"""

    minimo, maximo = obtener_rangos_atipicos(data_frame, columna)
    df = data_frame.loc[(data_frame[columna] <= minimo) | (data_frame[columna] >= maximo)]
    return df

def obtener_describe_dataframe(data_frame:'DataFarme', columnas_agrupacion:'list<str>', columna_informacion:str) -> dict:
    """Retorna un diccionario con los describe de los DataFrame agrupados eliminado las columnas con ceros

        Parámetros:
            data_frame (DataFarme): DataFrame que contiene la información
            columnas_agrupacion (list): Columnas que se usaran para la agrupación
            columna_informacion (str): Columna que se usara para realizar el describe

        Retorna:
            dict: Elementos del DataFrame agrupados con su describe:
                index(str):{
                    nombre:<str>, cantidad:<int>, promedio:<float>, minimo:<float>, maximo:<float>, desviacion:<float>
                }
    """
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
                    'cuartil_1':row['25%'],
                    'cuartil_3':row['75%'],
                    'desviacion':row['std']
                }

    return diccionario_de_estimaciones


def obtener_suma_columna_agrupada(data_frame:'DataFarme', columnas_agrupacion:'list<str>', columna_informacion:str, cantidad_retorno:int=10) -> dict:
    """
        Retorna un diccionario con la suma de los elementos agrupados de mayor a menor según la suma.

        Parámetros:
            data_frame (DataFarme): DataFrame que contiene la información
            columnas_agrupacion (list): Columnas que se usaran para la agrupación
            columna_informacion (str): Columna que se usara para realizar la suma
            cantidad_retorno (int, opcional): cantidad máxima de elementos retornar en el diccionario. Por defecto es 10.

        Retorna:
            dict: Elementos del DataFrame agrupados con su suma: {nombre:<str>, tiempo_total:<int>}
    """
    diccionario_de_estimaciones = dict()
    if not data_frame.empty:
        suma_columna_informacion = data_frame.groupby(columnas_agrupacion)[columna_informacion].sum()
        data_fame_ordenado = suma_columna_informacion.sort_values(ascending=False).head(cantidad_retorno).to_frame()
        
        for index, row in data_fame_ordenado.iterrows():
            row = row.fillna(0)
            diccionario_de_estimaciones[index] = {
                    'nombre':index,
                    'tiempo_total':row['tiempo_real'],
                }

    return diccionario_de_estimaciones


def obtener_suma_columna(data_frame:'DataFarme', columna_informacion:str) -> int:
    """
        Retorna la suma de los elementos en un DataFrame según la columna recibida como parámetro

        Parámetros:
            data_frame (DataFarme): DataFrame que contiene la información
            columna_informacion (str): Columna que se usara para realizar la suma

        Retorna:
            int: Suma de todos los elementos de la columna recibida como parámetro
    """
    suma_columna_informacion = 0
    if not data_frame.empty:
        suma_columna_informacion = data_frame[columna_informacion].sum()
    return suma_columna_informacion
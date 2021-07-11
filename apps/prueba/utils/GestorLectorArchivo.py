from abc import ABCMeta, abstractmethod
import pandas as pd

class GestorLectorArchivo(metaclass=ABCMeta):
    _ruta_archivo = None
    _dataframe = None

    def __init__(self, ruta_archivo, *args, **kwargs):
        self._ruta_archivo = ruta_archivo





    def obtener_dataframe(self) -> 'Dataframe':
        return self._dataframe
    

    def obtener_valores_columna(self, columna:str) -> 'list<str>':
        return self._dataframe[columna].unique().tolist()


    def obtener_descripcion_columna(self, columna_datos:str, columna_info:str):
        lista_datos = list()
        lista_valores = self.obtener_valores_columna(columna_datos)
        for valor in lista_valores:
            
            df = self._dataframe[self._dataframe[columna_datos].isin([valor])]
            df = df[[columna_datos, columna_info, 'Issue key']]
            df = self.eliminar_ceros(df)
            df_atipicos = self.obtener_valores_atipicos(df, columna_info)
            df_sin_atipicos = self.eliminar_valores_atipicos(df, columna_info)
            
            if not df.empty:
                lista_datos.append({'valor':valor, 'descripcion':df_sin_atipicos[columna_info].describe()})
        return lista_datos
    
 
    def eliminar_ceros(self, data_frame):
        df = data_frame[(data_frame != 0).all(1)]
        return df

    def obtener_rangos_atipicos(self, data_frame, columna_info):
        q1 = data_frame[columna_info].quantile(0.25) 
        q3 = data_frame[columna_info].quantile(0.75)
        iqr = q3-q1 #Rango intercuartil
        minimo  = q1-1.5*iqr 
        maximo = q3+1.5*iqr
        return (minimo, maximo)

    def eliminar_valores_atipicos(self, data_frame, columna_info):
        minimo, maximo = self.obtener_rangos_atipicos(data_frame, columna_info)
        df = data_frame.loc[(data_frame[columna_info] > minimo) & (data_frame[columna_info] < maximo)]
        return df
    
    def obtener_valores_atipicos(self, data_frame, columna_info):
        minimo, maximo = self.obtener_rangos_atipicos(data_frame, columna_info)
        df = data_frame.loc[(data_frame[columna_info] <= minimo) | (data_frame[columna_info] >= maximo)]
        return df

    
    def obtener_cantidad_y_suma(self, columna_datos, columna_info, maxima_cantidad):
        lista_datos = list()        
        cantidades = self.contar_cantidad_repetidos(columna_datos)   
        tiempos = self.sumar_valores_agrupados(columna_datos, columna_info)

        cantidad_actual = 0
        for cantidad in cantidades:
            if cantidad_actual <= maxima_cantidad:
                actividad_cantidad = cantidad['actividad']            
                for tiempo in tiempos:
                    actividad_tiempo = tiempo['actividad']
                    if actividad_tiempo in cantidad['actividad']:
                        lista_datos.append({'actividad':actividad_tiempo, 'cantidad':cantidad['cantidad'], 'tiempo':round(tiempo['cantidad'], 2)})
                        cantidad_actual += 1
                        break
            else:
                break
        return lista_datos
      
        

    def contar_cantidad_repetidos(self, columna_datos):
        lista_datos = list()        
        df = self._dataframe[columna_datos].value_counts()
        for index, value in df.items():            
            lista_datos.append({'actividad':index, 'cantidad':value})
        return lista_datos
    

    def sumar_valores_agrupados(self, columna_datos, columna_info):
        lista_datos = list()
        df = self._dataframe.groupby(columna_datos)[columna_info].sum()      
        for index, value in df.items():            
            lista_datos.append({'actividad':index, 'cantidad':value})
        return lista_datos

from .GestorLectorArchivo import GestorLectorArchivo

import pandas as pd
class GestorLectorExcel(GestorLectorArchivo):
      
    def __init__(self, ruta_archivo, *args, **kwargs):
        super(GestorLectorExcel, self).__init__(ruta_archivo=ruta_archivo)
       
        self.obtener_dataframe_de_archivo_excel()
    
    def obtener_dataframe_de_archivo_excel(self) -> 'Dataframe':
        """
            Retorna un dataframe usando un archivo de excel como parámetro

            Parámetros:
                archivo: archivo de excel que contiene la información 

            Retorno:
                Dataframe: dataframe
        """        

        self._dataframe = pd.read_excel(self._ruta_archivo, engine='openpyxl')       
        cols = self._dataframe.columns[~self._dataframe.columns.str.startswith('Unnamed:')]
        self._dataframe = self._dataframe[cols].dropna(how='all')

        

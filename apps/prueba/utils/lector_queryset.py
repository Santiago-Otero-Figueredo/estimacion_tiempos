from .GestorLectorArchivo import GestorLectorArchivo

import pandas as pd

class GestorLectorQueryset(GestorLectorArchivo):
      
    def __init__(self, ruta_archivo, *args, **kwargs):
        super().__init__(ruta_archivo=ruta_archivo)
       
        self.obtener_dataframe_de_queryset()
    
    def obtener_dataframe_de_queryset(self) -> 'Dataframe':
        """
            Retorna un dataframe usando un archivo de excel como parámetro

            Parámetros:
                archivo: archivo de excel que contiene la información 

            Retorno:
                Dataframe: dataframe
        """
        self._dataframe = pd.DataFrame(self._ruta_archivo)


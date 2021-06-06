from .GestorLectorArchivo import GestorLectorArchivo

class GestorLectorExcel(GestorLectorArchivo):
      
    def __init__(self, ruta_archivo, *args, **kwargs):
        super(GestorLectorExcel, self).__init__(ruta_archivo=ruta_archivo)
       
        self.modificar_dataframe()
        

    def modificar_dataframe(self) -> None:
        print("Modificar dataframe")
        
    
    def registrar_precios_desde_dataframe(self) -> None:
        print("Registra precios")
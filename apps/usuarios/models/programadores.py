from django.db import models

from apps.usuarios.models.usuarios import Usuario

class Programador(Usuario):

    @staticmethod
    def buscar_por_username(username:str) -> 'Programador':
        try:
            return Programador.objects.get(username=username)
        except Programador.DoesNotExist:
            return None
    
    def save(self):
        self.tipo = Usuario.PROGRAMADOR
        return super().save()
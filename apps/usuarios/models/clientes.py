from .usuarios import Usuario

class Cliente(Usuario):

    @staticmethod
    def buscar_por_username(username:str) -> 'Cliente':
        try:
            return Cliente.objects.get(username=username)
        except Cliente.DoesNotExist:
            return None
    
    def save(self):
        self.tipo = Usuario.CLIENTE
        return super().save()

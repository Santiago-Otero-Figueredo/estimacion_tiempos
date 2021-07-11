from apps.usuarios.models.usuarios import Usuario
from apps.usuarios.models.tipos_usuarios import TipoUsuario

class Administrador(Usuario):
    pass

    def save(self, *args, **kwargs):
        self.tipo_usuario = TipoUsuario.buscar_por_identificador(3)
        return super().save(*args, **kwargs)
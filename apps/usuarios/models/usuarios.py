# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from apps.utils.models import EstimacionModel


class Usuario(EstimacionModel, AbstractUser):

    tipo_documento = models.ForeignKey(
        'TipoDocumento',
        related_name="usuarios_asociados_documento",
        verbose_name="Tipo del documento",
        on_delete=models.SET_NULL,
        null=True
    )

    tipo_usuario = models.ForeignKey(
        'TipoUsuario',
        related_name="usuarios_asociados_tipo",
        verbose_name="Tipo del documento",
        on_delete=models.SET_NULL,
        null=True
    )

    email = models.EmailField(
        'Correo electrónico',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con ese correo.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{7,10}$',
        message="El numero de teléfono debe tener entre 7 y 10 digitos:"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Teléfono celular')

    is_verified = models.BooleanField(
        'Esta verificado',
        default=True,
        help_text='Cambiar a True cuando el usuario se haya verificado por correo electrónico.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password1', 'password2']
   
    def __str__(self):
        """Return username."""
        return self.username

    @classmethod
    def buscar_por_id(cls, id_elemento:int) -> 'Usuario':
        try:
            return cls.objects.get(pk=id_elemento)
        except cls.DoesNotExist:
            return cls.objects.none()


    @classmethod
    def existe_por_id(cls, id_elemento:int) -> bool:
        return cls.objects.filter(pk=id_elemento).exists()


    @classmethod
    def buscar_por_username(cls, username:str) -> 'Usuario':
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            return cls.objects.none()


    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)


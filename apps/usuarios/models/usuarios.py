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
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

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

    def save(self):
        self.username = self.email
        return super().save()


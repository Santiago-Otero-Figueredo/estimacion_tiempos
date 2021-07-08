from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

from apps.usuarios.forms import FormularioInicioSesion

class InicioSesion(LoginView):
    template_name = 'usuarios/sesion/inicio_sesion.html'
    form_class = FormularioInicioSesion
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('usuarios:iniciar_sesion')
        return super().dispatch(request, *args, **kwargs)

class CerrarSesion(LogoutView):
    template_name = 'usuarios/sesion/inicio_sesion.html'

@login_required
def logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect('inicio')
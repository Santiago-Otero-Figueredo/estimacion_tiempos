from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from apps.utils.clases.jira.ConexionJira import Jira

from apps.usuarios.forms import FormularioInicioSesion

class PaginaInicio(TemplateView):
    template_name = 'usuarios/sesion/pagina_inicio.html'

    def dispatch(self, request, *args, **kwargs):
        print("#-----------------------------")
        jira = Jira()
        #jira.consultar_historias_usuarios('PRIAL')
        jira.consultar_todos_los_proyectos()
        print("#-----------------------------")
        return super().dispatch(request, *args, **kwargs)


class InicioSesion(LoginView):
    template_name = 'usuarios/sesion/inicio_sesion.html'
    form_class = FormularioInicioSesion
    redirect_authenticated_user = True


class CerrarSesion(LogoutView):
    pass

@login_required
def logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect('inicio')
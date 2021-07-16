"""estimacion_tiempos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.usuarios.views import PaginaInicio

urlpatterns = [
    path('', PaginaInicio.as_view(), name='inicio'),
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('actividades/', include('apps.actividades.urls', namespace='actividades')),
    path('proyectos/', include('apps.proyectos.urls', namespace='proyectos')),
    path('estimaciones/', include('apps.estimaciones.urls', namespace='estimaciones')),
    path('pruebas/', include('apps.prueba.urls', namespace='pruebas')),
]

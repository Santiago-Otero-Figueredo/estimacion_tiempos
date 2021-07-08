from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from rest_framework.views import APIView
from rest_framework.response import Response
from config.settings.base import DIRECCION_HOST

from apps.estimaciones.models.actividades import Actividad
from apps.utils.mixin import MensajeMixin

from apps.estimaciones.forms import RegistrarActividadForm

class RegistrarActividad(MensajeMixin, CreateView):
    model = Actividad
    form_class = RegistrarActividadForm
    success_url = reverse_lazy("estimaciones:listado_actividades")
    template_name = "estimaciones/actividades/registrar.html"
    mensaje_exito = "La actividad ha sido registrada correctamente"
    mensaje_error = "Error registrar actividad, por favor verificar los datos"


class ListadoActividad(ListView):
    model = Actividad
    context_object_name = "actividades"
    template_name = "estimaciones/actividades/listado.html"


class ObtenerActividadesComunes(APIView):

    def get(self, request, format=None):
        parametros = self.request.GET

        nombre = parametros["nombre"]
        actividades = list(Actividad.obtener_actividades_por_nombre(nombre))

        print(actividades)
        return Response({
            "actividades": actividades,
        })
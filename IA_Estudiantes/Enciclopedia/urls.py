from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import lista_enciclopedia, subir_enciclopedia, editar_enciclopedia, eliminar_enciclopedia, EnciclopediaViewSet

router = DefaultRouter()
router.register(r'enciclopedia', views.EnciclopediaViewSet, basename='enciclopedia')

urlpatterns = [
    path("", include(router.urls)),
    path("editar/<int:enciclopedia_id>/", editar_enciclopedia, name="editar_enciclopedia"),
    path("eliminar/<int:enciclopedia_id>/", eliminar_enciclopedia, name="eliminar_enciclopedia"),
    path("subir/", subir_enciclopedia, name="subir_enciclopedia"),
    path("lista/", lista_enciclopedia, name="lista_enciclopedia"),
]
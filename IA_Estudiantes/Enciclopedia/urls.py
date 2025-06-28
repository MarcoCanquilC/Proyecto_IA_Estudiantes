from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import lista_enciclopedia, subir_enciclopedia

router = DefaultRouter()

urlpatterns = [
    path("subir/", subir_enciclopedia, name="subir_enciclopedia"),
    path("lista/", lista_enciclopedia, name="lista_enciclopedia"),
]
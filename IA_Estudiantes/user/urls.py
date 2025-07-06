from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet
from .views import ProgresoSemanalViewSet
from .views import mi_progreso
from .views import vista_progreso_usuario
from .views import toggle_favorito

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"progreso", ProgresoSemanalViewSet, basename="progreso")

urlpatterns = [
    path("", include(router.urls)),
    path("progreso/mio/", mi_progreso, name="mi_progreso"),
    path("favorito/<int:tema_id>/", toggle_favorito, name="toggle_favorito"),
]
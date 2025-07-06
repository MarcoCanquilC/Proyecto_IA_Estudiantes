from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core import views as core_views
from user import views as user_views
from Enciclopedia import views as enciclopedia_views

schema_view = get_schema_view(
   openapi.Info(
      title="API de IA Estudiantes",
      default_version='v1',
      description="Documentación de la API para el asistente educativo virtual",
      terms_of_service="https://www.tusitio.com/terminos/",
      contact=openapi.Contact(email="soporte@tusitio.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("smart/", core_views.vistaIAEstudiantes, name="vistaIA"),
    path("registroProfesores/", core_views.registroProfesores, name="vistaRegistroProfesores    "),
    path("herramientas/", core_views.herramientas, name="vistaHerramientas" ),
    path("", core_views.vistaIAEstudiantes, name="vistaIA"),
    path("temas/", core_views.temas, name="vistatemas" ),
     path("rendimiento/", user_views.vista_progreso_usuario, name="rendimiento_usuario"),
    path("cuestionario/", core_views.cuestionario, name="vistacuestionario" ),
    path("usuario/", include("user.urls")),
    path("enciclopedia/", include("Enciclopedia.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
  
]


#solo durante desarrollo
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:  # Solo para desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

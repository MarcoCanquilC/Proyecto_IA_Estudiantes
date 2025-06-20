"""
URL configuration for Natura_Web_DJ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



from core import views as core_views
from user import views as user_views

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
    path("api/users/", include("user.urls")),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("smart/", core_views.vistaIAEstudiantes, name="vistaIA"),
    path("registroProfesores/", core_views.registroProfesores, name="vistaRegistroProfesores    "),
    path("herramientas/", core_views.herramientas, name="vistaHerramientas" ),
    path("", core_views.vistaIAEstudiantes, name="vistaIA"),
    path("temas/", core_views.temas, name="vistatemas" ),
]


#solo durante desarrollo
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:  # Solo para desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

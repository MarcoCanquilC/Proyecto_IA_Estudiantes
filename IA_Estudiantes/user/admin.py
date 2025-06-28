from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ProgresoSemanal
from .models import tema, favorito
admin.site.register(ProgresoSemanal)


@admin.register(tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nivel")
    search_fields = ("nombre",)


@admin.register(favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tema", "fecha_agregado")
    list_filter = ("fecha_agregado",)
    search_fields = ("usuario__username", "tema__nombre")
    

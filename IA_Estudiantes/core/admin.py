from django.contrib import admin

from django.contrib import admin
from .models import tema, favorito

@admin.register(tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nivel")
    search_fields = ("nombre",)

@admin.register(favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tema", "fecha_agregado")
    list_filter = ("fecha_agregado",)
    search_fields = ("usuario__username", "tema__nombre")
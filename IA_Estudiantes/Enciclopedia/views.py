from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import EnciclopediaForm
from .models import Enciclopedia
from .serializers import EnciclopediaSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

#VIEWSET API PERMISSIONS

class EsDocenteOReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name="docentes").exists()

class EnciclopediaViewSet(viewsets.ModelViewSet):
    queryset = Enciclopedia.objects.all()
    serializer_class = EnciclopediaSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [EsDocenteOReadOnly]

#VISTAS
@login_required
def subir_enciclopedia(request):
    # Solo permitir si pertenece al grupo "docentes"
    if not request.user.groups.filter(name="docentes").exists():
        return HttpResponseForbidden("No tienes permiso para subir contenido.")
    
    if request.method == "POST":
        form = EnciclopediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_enciclopedia")
    else:
        form = EnciclopediaForm()
    return render(request, "subir_enciclopedia.html", {"form": form})

@login_required
def eliminar_enciclopedia(request, enciclopedia_id):
    if not request.user.groups.filter(name="docentes").exists():
        return HttpResponseForbidden("No tienes permiso para eliminar contenido.")
    
    enciclopedia = get_object_or_404(Enciclopedia, id=enciclopedia_id)
    enciclopedia.delete()
    return redirect("lista_enciclopedia")

@login_required
def editar_enciclopedia(request, enciclopedia_id):
    if not request.user.groups.filter(name="docentes").exists():
        return HttpResponseForbidden("No tienes permiso para editar contenido.")
    
    enciclopedia = get_object_or_404(Enciclopedia, id=enciclopedia_id)

    if request.method == "POST":
        form = EnciclopediaForm(request.POST, request.FILES, instance=enciclopedia)
        if form.is_valid():
            form.save()
            return redirect("lista_enciclopedia")
    else:
        form = EnciclopediaForm(instance=enciclopedia)

    return render(request, "editarEnciclopedia.html", {"form": form})

@login_required
def lista_enciclopedia(request):
    enciclopedias = Enciclopedia.objects.all()
    es_docente = request.user.groups.filter(name="docentes").exists()
    return render(request, "listar_enciclopedia.html", {
        "enciclopedias": enciclopedias,
        "es_docente": es_docente
    })



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


# Create your views here.

def vistaIAEstudiantes(request):
    return render(request, "IA.html")

def registroProfesores(request):
    return render (request, "registroProfesores.html")

def herramientas(request):
    return render(request, "herramientas.html")

def temas(request):
    return render(request, "temas.html")

def cuestionario(request):
    return render(request, "cuestionario.html")




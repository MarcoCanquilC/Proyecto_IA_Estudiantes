from django.shortcuts import render

# Create your views here.


def vistaIAEstudiantes(request):
    return render(request, "IA.html")

def registroProfesores(request):
    return render (request, "registroProfesores.html")

def herramientas(request):
    return render(request, "Herramientas.html")

def temas(request):
    return render(request, "temas.html")
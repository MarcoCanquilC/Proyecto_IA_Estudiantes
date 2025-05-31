from django.shortcuts import render

# Create your views here.


def vistaIAEstudiantes(request):
    return render(request, "IA.html")

def vistaInicioSesion(request):
    return render (request, "login.html")
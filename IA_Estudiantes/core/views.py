from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import tema, favorito


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

@login_required
def toggle_favorito(request, tema_id):
    tema = get_object_or_404(tema, id=tema_id)
    favorito, creado = favorito.objects.get_or_create(usuario=request.user, tema=tema)
    
    if not creado:
        # Ya existía → eliminar
        favorito.delete()
    return redirect("temas.html")  # Redirige donde quieras (p. ej. lista de temas)

def vista_principal(request):
    temas = tema.objects.all()
    favoritos = favorito.objects.filter(usuario=request.user).select_related("tema")
    return render(request, "temas.html", {
        "temas": temas,
        "favoritos": favoritos,
    })
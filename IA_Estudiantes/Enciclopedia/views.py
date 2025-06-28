from django.shortcuts import render, redirect
from .forms import EnciclopediaForm
from .models import Enciclopedia

def subir_enciclopedia(request):
    if request.method == "POST":
        form = EnciclopediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_enciclopedia")
    else:
        form = EnciclopediaForm()
    return render(request, "subir_enciclopedia.html", {"form": form})

def lista_enciclopedia(request):
    enciclopedias = Enciclopedia.objects.all()
    return render(request, "listar_enciclopedia.html", {"enciclopedias": enciclopedias})



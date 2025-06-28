import json
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import ProgresoSemanal
from .serializers import ProgresoSemanalSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets, permissions
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import tema, favorito
from django.shortcuts import get_object_or_404, redirect

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProgresoSemanalViewSet(viewsets.ModelViewSet):
    serializer_class = ProgresoSemanalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ProgresoSemanal.objects.none()
    
        if self.request.user.is_anonymous:
            return ProgresoSemanal.objects.none()

        return ProgresoSemanal.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado al guardar
        serializer.save(user=self.request.user)

def vista_progreso_usuario(request):
    try:
        progreso = request.user.progress
        notas_objetivos = progreso.notasObjetivos or {}
        notas_simulacros = progreso.notasSimulacros or {}
        avance_objetivo = progreso.avanceObjetivo or {}

        recomendaciones = []
        for asignatura, objetivo in notas_objetivos.items():
            nota = notas_simulacros.get(asignatura)
            if nota is not None and objetivo > nota:
                diferencia = objetivo - nota
                recomendaciones.append({
                    "asignatura": asignatura,
                    "diferencia": round(diferencia, 1)
                })

        return render(request, "rendimiento.html", {
            "progreso": progreso,
            "json_notas_objetivos": json.dumps(notas_objetivos),
            "json_notas_simulacros": json.dumps(notas_simulacros),
            "json_avance_objetivo": json.dumps(avance_objetivo),
            "recomendaciones": recomendaciones
        })
    except ProgresoSemanal.DoesNotExist:
        return render(request, "rendimiento.html", {"progreso": None})
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mi_progreso(request):
    try:
        progreso = request.user.progress  # Relación OneToOne
        serializer = ProgresoSemanalSerializer(progreso)
        return Response(serializer.data)
    except ProgresoSemanal.DoesNotExist:
        return Response({"detail": "No se encontró progreso para este usuario."}, status=status.HTTP_404_NOT_FOUND)

def vista_principal(request):
    temas = tema.objects.all()
    favoritos = favorito.objects.filter(usuario=request.user).select_related("tema")
    return render(request, "temas.html", {
        "temas": temas,
        "favoritos": favoritos,
    })

@login_required
def toggle_favorito(request, tema_id):
    tema = get_object_or_404(tema, id=tema_id)
    favorito, creado = favorito.objects.get_or_create(usuario=request.user, tema=tema)
    
    if not creado:
        # Ya existía → eliminar
        favorito.delete()
    return redirect("temas.html")  # Redirige donde quieras (p. ej. lista de temas)
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
        progreso = request.user.progress  # OneToOneField con related_name
    except ProgresoSemanal.DoesNotExist:
        progreso = None

    return render(request, "rendimiento.html", {"progreso": progreso})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mi_progreso(request):
    try:
        progreso = request.user.progress  # Relación OneToOne
        serializer = ProgresoSemanalSerializer(progreso)
        return Response(serializer.data)
    except ProgresoSemanal.DoesNotExist:
        return Response({"detail": "No se encontró progreso para este usuario."}, status=status.HTTP_404_NOT_FOUND)


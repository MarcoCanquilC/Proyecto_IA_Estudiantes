from django.db import models
from django.contrib.auth.models import User
from .metricas import (
    calcular_avance_objetivo,
    calcular_porcentaje_temas,
)

class ProgresoSemanal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="progress")
    horasSemanales = models.PositiveIntegerField(default=0)
    topicosCubiertos = models.PositiveIntegerField(default=0)
    totalTopicos = models.PositiveIntegerField(default=0)
    sesionesEstudio = models.PositiveIntegerField(default=0)
    tiempoPromedioPorSesion = models.PositiveIntegerField(default=0)
    tiempoPromedioGeneral = models.PositiveIntegerField(default=0)
    porcentajeObjetivosCumplidos = models.FloatField(default=0.0)
    puntuacionAutodiagnostico = models.FloatField(default=0.0)
    erroresComunes = models.PositiveIntegerField(default=0)
    ultimaFechaActualizacion = models.DateTimeField(auto_now=True)
    
    notasObjetivos = models.JSONField(
    default=dict,
    help_text="Formato: {'matematicas': 650, 'lenguaje': 720, ...}"
    )

    notasSimulacros = models.JSONField(
    default=dict,
    help_text="Formato: {'matematicas': 650, 'lenguaje': 720, ...}"
    )

    avanceObjetivo = models.JSONField(
    default=dict,
    help_text="Ej: {'matematicas': 0.8, 'lenguaje': 0.6}"
    )
    # Usamos JSONField para registrar el progreso por asignatura
    subjectProgress = models.JSONField(
        default=dict, 
        help_text="Formato: {'matematicas': 50, 'lenguaje': 70, 'ciencias': 40, 'historia': 90}"
    )

    def __str__(self):
        return f"Progreso de {self.user.username}"

    def save(self, *args, **kwargs):
        self.avanceObjetivo = calcular_avance_objetivo(self.notasSimulacros, self.notasObjetivos)
        self.porcentajeObjetivosCumplidos = calcular_porcentaje_temas(self.topicosCubiertos, self.totalTopicos)
        super().save(*args, **kwargs)



class tema(models.Model):
    nombre = models.CharField(max_length=200)
    nivel = models.CharField(max_length=50, choices=[
        ("Básico", "Básico"),
        ("Intermedio", "Intermedio"),
        ("Avanzado", "Avanzado")
    ])
    descripcion = models.TextField(blank=True)  # opcional, si después quieres meter más info

    def __str__(self):
        return f"{self.nombre} ({self.nivel})"

class favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.ForeignKey(tema, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'tema')  # Para que un usuario no agregue el mismo tema más de una vez

    def __str__(self):
        return f"{self.usuario.username} ♥ {self.tema.nombre}"

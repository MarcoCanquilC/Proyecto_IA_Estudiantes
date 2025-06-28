from django.db import models
from django.contrib.auth.models import User

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

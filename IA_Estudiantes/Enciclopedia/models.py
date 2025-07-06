from django.db import models

class Enciclopedia(models.Model):

    CATEGORIAS = [
        ("Fisica", "Física"),
        ("Quimica", "Química"),
        ("Matematica", "Matemática"),
        ("Biologia", "Biología"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    imagen = models.ImageField(upload_to='enciclopedia/', blank=True, null=True)
    archivo = models.FileField(upload_to="uploads/")
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, null=True, blank=True)









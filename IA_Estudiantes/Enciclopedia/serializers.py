from rest_framework import serializers
from .models import Enciclopedia

class EnciclopediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enciclopedia
        fields = ["id", "nombre", "descripcion", "fecha_creacion", "fecha_actualizacion", "imagen", "archivo"]
        read_only_fields = ["fecha_creacion", "fecha_actualizacion"]
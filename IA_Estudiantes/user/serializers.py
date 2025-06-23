from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProgresoSemanal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff"]

class ProgresoSemanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoSemanal
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        return ProgresoSemanal.objects.create(**validated_data)
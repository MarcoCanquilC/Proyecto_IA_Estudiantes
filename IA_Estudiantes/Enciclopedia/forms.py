from django import forms
from .models import Enciclopedia

class EnciclopediaForm(forms.ModelForm):
    class Meta:
        model = Enciclopedia
        fields = ["nombre", "descripcion", "imagen", "archivo"]

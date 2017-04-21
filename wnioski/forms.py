from django.forms import ModelForm
from .models import Pracownik


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = ('imie', 'nazwisko')

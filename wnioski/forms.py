from django.forms import ModelForm
from .models import Pracownik, Wniosek


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = ('imie', 'nazwisko', 'data_zatr')


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'data_zlo', 'prac_sklada', 'prac_dot', 'obiekt')

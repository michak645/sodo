from django.forms import ModelForm
from .models import Pracownicy, Wnioski


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownicy
        fields = ('imie', 'nazwisko', 'data_zatr')


class WniosekForm(ModelForm):
    class Meta:
        model = Wnioski
        fields = ('typ', 'data_zlo', 'prac_sklada', 'prac_dot', 'obiekt')

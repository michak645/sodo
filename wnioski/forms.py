from django.forms import ModelForm
from .models import Wniosek, Obiekt, TypObiektu
from django import forms
from auth_ex.models import JednOrg, Pracownik


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'pracownik', 'obiekt')

    def __init__(self, *args, **kwargs):
        super(WniosekForm, self).__init__(*args, **kwargs)
        # self.fields['prac_sklada'].initial = args


class SearchForm(forms.Form):
    username = forms.CharField(max_length=100)


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = (
            'imie', 'nazwisko', 'email', 'data_zatr', 'szkolenie',
            'rodzaj', 'jedn_org', 'login', 'haslo'
        )


class ObiektForm(ModelForm):
    class Meta:
        model = Obiekt
        fields = (
            'nazwa', 'typ', 'jedn_org', 'opis'
        )


class TypeForm(ModelForm):
    class Meta:
        model = TypObiektu
        fields = ('nazwa', )


class JednostkaForm(ModelForm):
    class Meta:
        model = JednOrg
        fields = ('id_jedn', 'nazwa')


class EditPracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = (
            'imie', 'nazwisko', 'email', 'data_zatr',
            'szkolenie', 'rodzaj', 'jedn_org', 'login', 'haslo'
        )


class EditObiektForm(ModelForm):
    class Meta:
        model = Obiekt
        fields = (
            'nazwa', 'typ', 'jedn_org', 'opis'
        )


class EditWniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'pracownik', 'obiekt')


class EditTypObiektuForm(ModelForm):
    class Meta:
        model = TypObiektu
        fields = ('nazwa', )


class EditJednostkaForm(ModelForm):
    class Meta:
        model = JednOrg
        fields = ('id_jedn', 'nazwa')

from django.forms import ModelForm
from .models import Wniosek, Obiekt, TypObiektu
from django import forms

from multiselectfield import MultiSelectField


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ',)

    # def clean_user(self):
    #     user = self.cleaned_data['user']
    #     return user


class SearchForm(forms.Form):
    username = forms.CharField(max_length=100)


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


class EditObiektForm(ModelForm):
    class Meta:
        model = Obiekt
        fields = (
            'nazwa', 'typ', 'jedn_org', 'opis'
        )


class EditWniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'pracownik', 'obiekty')


class EditTypObiektuForm(ModelForm):
    class Meta:
        model = TypObiektu
        fields = ('nazwa', )


class ObiektFiltrowanieForm(forms.Form):
    uprawnienia_choices = (
        ('1', 'Wgląd'),
        ('2', 'Tworzenie'),
        ('3', 'Modyfikacja'),
        ('4', 'Przetwarzanie na serwerze i w biurze'),
        ('5', 'Przechowywanie'),
        ('6', 'Usuwanie, niszczenie'),
        ('7', 'Udostępnianie, powierzanie, przesyłanie'),
    )
    jednostka = forms.CharField(max_length=100, required=False)
    pracownik = forms.CharField(max_length=100, required=False)
    uprawnienia = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=uprawnienia_choices,
        required=False,
    )

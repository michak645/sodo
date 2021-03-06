from django import forms

from wnioski.models import Wniosek
from auth_ex.models import JednOrg, Pracownik


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Wniosek
        fields = ['pracownik', 'typ', 'uprawnienia', 'obiekty']
        widgets = {
            'pracownik': forms.HiddenInput(),
            'uprawnienia': forms.CheckboxSelectMultiple(),
        }


class WizardObiekt(forms.Form):
    jednostka = forms.ModelChoiceField(
        queryset=JednOrg.objects.all(), empty_label=None)


class WizardPracownik(forms.Form):
    pracownik = forms.ModelChoiceField(
        queryset=Pracownik.objects.all(), empty_label=None)


class WizardUprawnienia(forms.Form):
    uprawnienia_choices = (
        ('1', 'Wgląd'),
        ('2', 'Tworzenie'),
        ('3', 'Modyfikacja'),
        ('4', 'Przetwarzanie na serwerze i w biurze'),
        ('5', 'Przechowywanie'),
        ('6', 'Usuwanie, niszczenie'),
        ('7', 'Udostępnianie, powierzanie, przesyłanie'),
    )
    typ_choices = (
        ('1', 'Nadanie uprawnień'),
        ('2', 'Odebranie uprawnień'),
    )
    uprawnienia = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=uprawnienia_choices)
    typ_wniosku = forms.ChoiceField(
        choices=typ_choices, required=True,
        widget=forms.RadioSelect())

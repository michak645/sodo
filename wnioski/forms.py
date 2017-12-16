from django.forms import ModelForm
from .models import Wniosek, Obiekt, TypObiektu
from django import forms


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'uprawnienia', 'pracownik', 'obiekt')
        widgets = {
            'uprawnienia': forms.Select(),
        }

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
        fields = ('typ', 'pracownik', 'obiekt')


class EditTypObiektuForm(ModelForm):
    class Meta:
        model = TypObiektu
        fields = ('nazwa', )

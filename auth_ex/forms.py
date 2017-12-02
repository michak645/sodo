from django import forms
from django.contrib.auth.models import User

from auth_ex.models import Pracownik


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
            'first_name': forms.
        }


class PracownikForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = ['data_zatr', 'jedn_org', 'rodzaj', 'szkolenie']
        widgets = {
            'data_zatr': forms.SelectDateWidget(),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from auth_ex.models import Pracownik


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(),
        }


class PracownikForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = ['data_zatr', 'jedn_org', 'rodzaj', 'szkolenie']
        widgets = {
            'data_zatr': forms.SelectDateWidget(),
        }

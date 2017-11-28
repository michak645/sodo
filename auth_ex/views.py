from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from wnioski.models import Pracownik


class LoginFormView(View):
    def post(self, request):
        login = request.POST['login']
        password = request.POST['password']
        user = get_object_or_404(
            Pracownik,
            login=login,
            haslo=password)

        if user is not None:
            return HttpResponseRedirect('/wnioski/')
        else:
            return HttpResponseRedirect('/wnioski/')

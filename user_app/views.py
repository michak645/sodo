from django.shortcuts import render

from auth_ex.models import Pracownik


def user_index(request):
    pracownik = Pracownik.objects.get(id=request.session['pracownik'])
    context = {
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_index.html', context)


def user_applications(request):
    return render(request, 'user_app/user_applications.html')


def user_add_app(request):
    return render(request, 'user_app/user_add_app.html')

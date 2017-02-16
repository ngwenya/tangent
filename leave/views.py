from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from settings import base as settings


def login_view(request):

    template = 'leave/user_login.html',
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_URL)
        else:
            form = LoginForm()

    return render(request, template, {'login_form': form})


def logout_view(request):
    logout(request)

    return redirect(settings.LOGOUT_REDIRECT_URL)


def dashboard(request):

    template = 'leave/dashboard.html'

    return render(request, template)

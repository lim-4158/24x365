from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

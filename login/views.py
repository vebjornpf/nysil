from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse
from .forms import UserForm

# Create your views here.



def index(request):
    return render(request, "login.html", {})


    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'http://127.0.0.1:8000/main', {})
            else:
                return render(request, 'http://127.0.0.1:8000/main/login', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'http://127.0.0.1:8000/main/login', {'error_message': 'Invalid login'})
    return render(request, 'http://127.0.0.1:8000/main/login')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'http://127.0.0.1:8000/main/', {})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)

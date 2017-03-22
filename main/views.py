from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View
from django.http import HttpResponse
<<<<<<< HEAD
from .forms import UserForm, ProfessorForm
=======
from .forms import UserForm
>>>>>>> master
from .models import Subject


# view for the header, which gonna be the same everywhere in the web page
def index(req):
    subjects = Subject.objects.all()
<<<<<<< HEAD
    print(subjects)
    return render(req, 'main/header.html',{'subjects_list': subjects})


def index2(request):
    return render(request, "main/login.html", {})
=======
    return render(req, 'main/header.html',{'subject_list': subjects})
>>>>>>> master

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'main/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
<<<<<<< HEAD
                return render(request, 'main/login.html', {})
=======
                return HttpResponseRedirect(reverse('main:index'))
>>>>>>> master
            else:
                return render(request, 'main/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'main/login.html', {'error_message': 'Invalid login'})
    return render(request, 'main/login.html')


<<<<<<< HEAD
def userregister(request):
=======
def register(request):
>>>>>>> master
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
                return render(request, 'main/header.html', {})
    context = {
        "form": form,
    }
<<<<<<< HEAD
    return render(request, 'main/userregister.html', context)

def professorregister(request):
    form = ProfessorForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        key = request.POST['key']
        if key != 'abc12345':
            return render(request, 'main/professorregister.html',{'form':form})
        user.set_password(password)
        user.is_staff=True
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'main/header.html', {})
    context = {
        "form": form,
    }
    return render(request, 'main/professorregister.html', context)



=======
    return render(request, 'main/register.html', context)
>>>>>>> master

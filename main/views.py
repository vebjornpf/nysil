from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import Subject, StudentConnectSubject

from django.db.models import Q


# view for the header, which gonna be the same everywhere in the web page
def index(req):
    return render(req,'main/header.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {"form": form}
    return HttpResponseRedirect(reverse('main:index'))


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
            else:
                return render(request, 'main/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'main/login.html', {'error_message': 'Invalid login'})
    return render(request, 'main/login.html')


def userregister(request):
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

    return render(request, 'main/register.html', context)


def professorregister(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        key = request.POST['key']
        if key != 'abc12345':
            return render(request, 'main/professorregister.html', {'form':form, 'error_message': 'Invalid activation key'},)
        user.is_staff = True
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'main/adminok.html', {})
    context = {
        "form": form,
    }
    return render(request, 'main/professorregister.html', context)

def search(request):
    query = request.GET.get('q')
    if query is not None and query != '' and request.is_ajax():
        subjects = Subject.objects.filter(
            Q(subject_code__icontains=query)
        )

        # you also can limit the maximum of `posts` here.
        # eg: posts[:50]
        return render(request, 'main/search.html',{'subjects': subjects})
    return render(request, 'main/search.html')

    return render(request, 'main/userregister.html', context)

def add_subject(request, subject_pk):
    user = request.user
    user.userprofile.add_subject(subject_pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

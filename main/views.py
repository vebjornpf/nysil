from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm
from .models import Subject

from django.db.models import Q


# view for the frontpage
def index(req):
    return render(req,'main/header.html')

# method uses to logout a user, an redirects to the frontpage
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

# method uses to login a user
def login_user(request):
    if request.method == "POST":
        # logic to get the typed in username and password
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

# method for register a student
def userregister(request):
    form = UserForm(request.POST or None)
    if form.is_valid(): # form.is_valid() checks that tha form is on the correct format
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm = request.POST['confirm']
        if confirm != password:
            return render(request, 'main/userregister.html',{'form': form, 'error_message': 'Password not equal'}, )
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))

    context = {
        "form": form,
    }

    return render(request, 'main/userregister.html', context)

# method for register a professor, almost the same as userregister but the activation_key-input has to be corrext
# so all professors needs the activation_key to be an admin
def professorregister(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm = request.POST['confirm']
        if confirm != password:
            return render(request, 'main/professorregister.html', {'form': form, 'error_message': 'Password not equal'}, )
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
                return HttpResponseRedirect(reverse('main:index'))
    context = {
        "form": form,
    }
    return render(request, 'main/professorregister.html', context)

# method for the search-functionality. Used to search for a subject to follow
def search(request):
    user = request.user

    query = request.GET.get('q')
    if query is not None and query != '' and request.is_ajax():
        subjects = Subject.objects.filter(
            Q(subject_name__icontains=query)|Q(subject_code__icontains=query    )

        )

        # you also can limit the maximum of `posts` here.
        # eg: posts[:50]
        context = {'user': user, 'subjects':subjects}
        return render(request, 'main/search.html',context)
    return render(request, 'main/search.html')

# functionallity for adding a sujbject
def add_subject(request, subject_pk):
    user = request.user
    user.userprofile.add_subject(subject_pk)
    # this response makes sure that user gets redirected to the last visited page after adding a subject
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

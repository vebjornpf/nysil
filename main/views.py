from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Subject


def index(req):
    subjects = Subject.objects.all()
    print(subjects)
    return render(req, 'main/header.html',{'subjects_list': subjects})
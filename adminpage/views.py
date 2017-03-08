from django.shortcuts import render
from main.models import Subject, Chapter
from .forms import SubjectForm

def admin_index(req):
    return render(req,'adminpage/admin_header.html')

def subject_overview(req):
    subjects = Subject.objects.all()
    context = {'subjects':subjects}
    return render(req,'adminpage/subject_overview.html',context)

def chapter_overview(req,subject_pk):
    subjects = Subject.objects.all()
    subject = Subject.objects.get(pk=subject_pk)
    context = {'subject':subject,'subjects':subjects}
    return render(req,'adminpage/chapter_overview.html',context)

def new_subject(req):
    form = SubjectForm()
    subjects = Subject.objects.all()
    context = {'form':form, 'subjects': subjects}
    return render(req, 'adminpage/new_subject.html', context)



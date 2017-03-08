from django.shortcuts import render
from main.models import Subject, Chapter
from .forms import SubjectForm, ChapterForm
from django.http import HttpResponseRedirect
from django.urls import reverse


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

def new_chapter(request, subject_pk):
    subject = Subject.objects.get(pk=subject_pk)
    subjects = Subject.objects.all()
    form = ChapterForm(request.POST or None)
    context = {'form': form, 'subjects': subjects, 'subject': subject}

    # if the from is valid the created modelform will be saved in the database and the amdin
    # will be redirected to the chapter_overview
    if form.is_valid():
        # instance iss a Subject-object
        instance = form.save(commit=False)
        # forces the instace to set the subject (foreign) to the subject we have cliked on
        instance.subject = subject
        instance.save()
        return HttpResponseRedirect(reverse('adminpage:chapter_overview',args=(subject_pk,)))

    return render(request, 'adminpage/new_chapter.html', context)

def delete_chapter(request, subject_pk, chapter_pk):
    Chapter.objects.get(pk=chapter_pk).delete() # deletes the chapter we have clicked to delete
    return HttpResponseRedirect(reverse('adminpage:chapter_overview',args=(subject_pk,)))





from django.shortcuts import render
from main.models import Subject, Chapter, Exercise_Page
from .forms import SubjectForm, ChapterForm, ExerciseForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def admin_index(req):
    return render(req,'adminpage/admin_header.html')

def tilbakemeldinger(req):
    subjects = Subject.objects.all()
    context = {'subjects':subjects}
    return render(req,'adminpage/tilbakemeldinger.html',context)

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
    subjects = Subject.objects.all()
    form = SubjectForm(req.POST or None)
    context = {'form':form, 'subjects': subjects}

    # if the from is valid the created modelform will be saved in the database and the amdin
    # will be redirected to the subject_overview
    if form.is_valid():
        # instance iss a Subject-object
        instance = form.save(commit=False)
        # forces the instace to set the subject (foreign) to the subject we have cliked on
        instance.subjects = subjects
        instance.save()
        return HttpResponseRedirect(reverse('adminpage:subject_overview'))

    return render(req, 'adminpage/new_subject.html', context)

def delete_subject(request, subject_pk):
    Subject.objects.get(pk=subject_pk).delete() # deletes the subject we have clicked to delete
    return HttpResponseRedirect(reverse('adminpage:subject_overview'))

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


def exercise_overview(request, subject_pk, chapter_pk):
    subjects = Subject.objects.all()
    subject = Subject.objects.get(pk=subject_pk)
    chapter = Chapter.objects.get(pk=chapter_pk)

    context = {'subjects': subjects, 'subject': subject, 'chapter': chapter}
    return render(request, 'adminpage/exercise_overview.html', context)


def new_exercise(request, subject_pk, chapter_pk):
    subjects = Subject.objects.all()
    subject = Subject.objects.get(pk=subject_pk)
    chapter = Chapter.objects.get(pk=chapter_pk)
    form = ExerciseForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.chapter = chapter
        instance.save()
        return HttpResponseRedirect(reverse('adminpage:exercise_overview',args=(subject_pk,chapter_pk)))

    context = {'subjects': subjects, 'subject': subject, 'chapter': chapter, 'form': form}

    return render(request, 'adminpage/new_exercise.html', context)


def delete_exercise(request, subject_pk, chapter_pk, exercise_pk):
    Exercise_Page.objects.get(pk=exercise_pk).delete()
    return HttpResponseRedirect(reverse('adminpage:exercise_overview',args=(subject_pk, chapter_pk,)))







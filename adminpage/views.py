from django.shortcuts import render
from main.models import Subject, Chapter, Exercise_Page, StudentConnectExercise, StudentConnectSubject
from .forms import SubjectForm, ChapterForm, ExerciseForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User



def admin_index(req):
    user = req.user
    context = {'user':user}
    if user.is_staff==True:
        return render(req, 'adminpage/admin_header.html', context)
    else:
        return HttpResponseRedirect(reverse('main:index'))

def tilbakemeldinger(req):
    user = req.user
    subjects = Subject.objects.all()
    context = {'subjects':subjects}
    if user.is_staff==True:
        return render(req, 'adminpage/tilbakemeldinger.html', context)
    else:
        return HttpResponseRedirect(reverse('main:index'))

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
    deleted_chapter = Chapter.objects.get(pk=chapter_pk)
    for exercise in deleted_chapter.exercise_page_set.all():
        delete_exercise_points(exercise,subject_pk)
    deleted_chapter.delete() # deletes the chapter we have clicked to delete
    return HttpResponseRedirect(reverse('adminpage:chapter_overview',args=(subject_pk,)))


# view to change fields in chapter if admin for instance has typed wrong
def change_chapter(request, subject_pk, chapter_pk):
    subject = Subject.objects.get(pk=subject_pk)
    subjects = Subject.objects.all()
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    form = ChapterForm(request.POST or None, instance=chapter)
    context = {'subject': subject, 'subjects': subjects, 'form': form, 'chapter': chapter}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse('adminpage:chapter_overview', args=(subject_pk,)))

    return render(request, 'adminpage/change_chapter.html', context)




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

        user_subject_conn = StudentConnectSubject.objects.filter(subject=subject)
        for conn in user_subject_conn:
            connection = StudentConnectExercise(user=conn.user, exercise=instance)
            find_connection = StudentConnectExercise.objects.filter(user=conn.user, exercise=instance).exists()
            if not find_connection:
                connection.save()

        return HttpResponseRedirect(reverse('adminpage:exercise_overview',args=(subject_pk,chapter_pk)))

    context = {'subjects': subjects, 'subject': subject, 'chapter': chapter, 'form': form}

    return render(request, 'adminpage/new_exercise.html', context)

def change_exercise(request, subject_pk, chapter_pk, exercise_pk):
    subjects = Subject.objects.all()
    subject = Subject.objects.get(pk=subject_pk)
    chapter = Chapter.objects.get(pk=chapter_pk)
    exercise = get_object_or_404(Exercise_Page, pk=exercise_pk)
    form = ExerciseForm(request.POST or None, instance=exercise)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.chapter = chapter
        instance.save()
        return HttpResponseRedirect(reverse('adminpage:exercise_overview',args=(subject_pk,chapter_pk)))

    context = {'subjects': subjects, 'subject': subject, 'chapter': chapter, 'form': form, 'exercise': exercise}

    return render(request, 'adminpage/change_exercise.html', context)



def delete_exercise(request, subject_pk, chapter_pk, exercise_pk):
    deleted_exercise = Exercise_Page.objects.get(pk=exercise_pk)

    delete_exercise_points(deleted_exercise, subject_pk)
    return HttpResponseRedirect(reverse('adminpage:exercise_overview',args=(subject_pk, chapter_pk,)))


def chapters(req,subject_pk):
    subjects = Subject.objects.all()
    subject = Subject.objects.get(pk=subject_pk)
    context = {'subject':subject,'subjects':subjects}
    return render(req,'adminpage/chapters.html',context)

def chapter_feedback(req, subject_pk, chapter_pk):
    subjects = Subject.objects.all()
    chapter = Chapter.objects.get(pk=chapter_pk)
    subject = Subject.objects.get(pk=subject_pk)
    context = {'chapter': chapter, 'subject': subject, 'subjects': subjects}
    return render(req, 'adminpage/chapter_feedback.html', context)




# ------------------- HELP-METHODS -----------------------

def delete_exercise_points(deleted_exercise, subject_pk):
    # if you delete an exercise, the students who have answered it has to loose the points
    connections = StudentConnectExercise.objects.filter(exercise=deleted_exercise)
    for connection in connections:
        user = connection.user
        user_subject = StudentConnectSubject.objects.get(user=user, subject=Subject.objects.get(pk=subject_pk))
        if connection.completed_easy == True:
            user_subject.points -= deleted_exercise.easy_points
            user_subject.save()
        if connection.completed_medium == True:
            user_subject.points -= deleted_exercise.medium_points
            user_subject.save()
        if connection.completed_hard == True:
            user_subject.points -= deleted_exercise.hard_points
            user_subject.save()

    deleted_exercise.delete()
from django.shortcuts import render, get_object_or_404

# Create your views here.
from main.models import Subject, Theme, Exercise_Page

# this view is the "header" for the subject-pages
# its the same as main/header.html but has a sidebare too
def subject_view(req, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk) # the subject that was chosen
    # need a reference to subjects so they show up in the "Mine Fag"-dropdown menu
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/subject_header.html',{'subject_list': subjects,'subject':subject})


def all_exercises_view(req,theme_pk, subject_pk):
    theme = Theme.objects.get(pk=theme_pk)
    subject = Subject.objects.get(pk=theme.subject.pk)
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/chapter_page.html', {'subject_list': subjects,'theme':theme,
                                                         'subject':subject})


def exercise_view(req,theme_pk, subject_pk, exercise_pk):
    exercise = get_object_or_404(Exercise_Page, pk=exercise_pk)
    theme = exercise.theme
    subject = theme.subject
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/exercise_page.html', {'subject_list': subjects,'exercise' :exercise,'theme':theme,
                                                         'subject':subject})

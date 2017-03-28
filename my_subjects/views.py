from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from main.models import Subject, Chapter, Exercise_Page, StudentConnectExercise, StudentConnectSubject
from .forms import EasyAnswer, MediumAnswer, HardAnswer, CommentForm

# this view is the "header" for the subject-pages
# its the same as main/header.html but has a sidebare too

@login_required
def subject_view(req, subject_pk):
    user = req.user
    subject = get_object_or_404(Subject, pk=subject_pk) # the subject that was chosen
    # need a reference to subjects so they show up in the "Mine Fag"-dropdown menu
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/subject_header.html',{'subject_list': subjects,'subject':subject, 'user': user})


# this view shows alle det exercise_pages that have been added to a specific chapter
def all_exercises_view(req,chapter_pk, subject_pk):
    user = req.user
    chapter = Chapter.objects.get(pk=chapter_pk)
    subject = Subject.objects.get(pk=chapter.subject.pk)
    subjects = Subject.objects.all()

    exercises = chapter.exercise_page_set.all()
    connections = []
    for exercise in exercises:
        connections.append(StudentConnectExercise.objects.get(user=user,exercise=exercise))
        print(StudentConnectExercise.objects.get(user=user,exercise=exercise).exercise.headline)
    return render(req, 'my_subjects/chapter_page.html', {'subject_list': subjects,'chapter':chapter,
                                                         'subject':subject, 'connections': connections})



# every time the user has submitted an answer the exercise_view will be called
# cleaned_data is a method that gives us the value to the attributes we use
    # without cleaned data: ditt_svar = <input id="id_ditt_svar" name="ditt_svar" type="text" value="2" required />
    # with cleande data: ditt_svar = 2
def exercise_view(request,chapter_pk, subject_pk, exercise_pk):
    user = request.user
    exercise = get_object_or_404(Exercise_Page, pk=exercise_pk)
    chapter = exercise.chapter
    subject = chapter.subject
    subjects = Subject.objects.all()
    connection = StudentConnectExercise.objects.get(user=user,exercise=exercise)
    subject_connection = StudentConnectSubject.objects.get(user=user, subject=subject)
    form = EasyAnswer()  # doesnt matter what type of form this is. This is just to enable the form in the questions
    comment_form = CommentForm(request.POST or None)
    context = {'connection': connection, 'comment_form': comment_form, 'form': form, 'subject_list': subjects, 'exercise': exercise,
               'chapter': chapter,
               'subject': subject}

    if comment_form.is_valid():
        instance = comment_form.save(commit=False)
        instance.publisher = request.user
        instance.chapter = Chapter.objects.get(pk=chapter_pk)
        instance.exercise = Exercise_Page.objects.get(pk=exercise_pk)
        instance.save()
        return HttpResponseRedirect(reverse('my_subjects:exercise_view',args=(subject_pk,chapter_pk,exercise_pk,)))


    if request.method == 'POST':

        if 'easy' in request.POST:
            form = EasyAnswer(request.POST or None)
            if form.is_valid():
                answer = form.cleaned_data['ditt_svar']
                if (answer == exercise.easy_answer):
                    # do some logic for checking the easy answer
                    subject_connection.points += exercise.easy_points
                    subject_connection.save()
                    connection.completed_easy = True
                    connection.save()
        elif 'medium' in request.POST:
            form = MediumAnswer(request.POST or None)
            if form.is_valid():
                answer = form.cleaned_data['ditt_svar']
                if (answer == exercise.medium_answer):
                    # do some more logic
                    subject_connection.points += exercise.medium_points
                    subject_connection.save()
                    connection.completed_medium = True
                    connection.save()

        elif 'hard' in request.POST:
            form = HardAnswer(request.POST or None)
            if form.is_valid():
                answer = form.cleaned_data['ditt_svar']

                if (answer == exercise.hard_answer):
                    # do some more logic
                    subject_connection.points += exercise.hard_points
                    subject_connection.save()
                    connection.completed_hard = True
                    connection.save()
    return render(request, 'my_subjects/exercise_page.html', context)

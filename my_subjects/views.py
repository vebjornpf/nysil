from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import Subject, Chapter, Exercise_Page, StudentConnectExercise, StudentConnectSubject
from .forms import EasyAnswer, MediumAnswer, HardAnswer, CommentForm

# this view is the "header" for the subject-pages
# its the same as main/header.html but has a sidebare too


def subject_view(req, subject_pk):
    user = req.user
    subject = get_object_or_404(Subject, pk=subject_pk) # the subject that was chosen
    # need a reference to subjects so they show up in the "Mine Fag"-dropdown menu
    subjects = Subject.objects.all()
    if user.is_authenticated() == True:
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

    # attributes that renders so users easily can se which tasks are completed/not completed
    info_easy = "(Completed)" if connection.completed_easy==True else "(Not completed)"
    info_medium = "(Completed)" if connection.completed_medium == True else "(Not completed)"
    info_hard = "(Completed)" if connection.completed_hard == True else "(Not completed)"

    subject_connection = StudentConnectSubject.objects.get(user=user, subject=subject)
    form = EasyAnswer()  # doesnt matter what type of form this is. This is just to enable the form in the questions
    comment_form = CommentForm(request.POST or None)

    info = ""

    context = {'connection': connection, 'comment_form': comment_form, 'form': form, 'subject_list': subjects, 'exercise': exercise,
               'chapter': chapter,
               'subject': subject,
               'info_easy': info_easy,
               'info_medium': info_medium,
               'info_hard': info_hard}

    if comment_form.is_valid():
        instance = comment_form.save(commit=False)
        instance.publisher = request.user
        instance.chapter = Chapter.objects.get(pk=chapter_pk)
        instance.exercise = Exercise_Page.objects.get(pk=exercise_pk)
        instance.save()
        return HttpResponseRedirect(reverse('my_subjects:exercise_view',args=(subject_pk,chapter_pk,exercise_pk,)))


    if request.method == 'POST':

        # LOGIC FOR CHECKING THE EASY ANSWER
        if 'easy' in request.POST:
            form = EasyAnswer(request.POST or None)
            if form.is_valid():
                question = exercise.easy_question
                context['question'] = question
                context['form'] = form
                answer = form.cleaned_data['your_answer']
                context['answer'] = answer
                answerlist = answer.split(' ')
                easy_answer_list = exercise.easy_answer.split(' ')

                if set(easy_answer_list).issubset(set(answerlist)):
                    if connection.completed_easy == False:
                        info += "You answered correct, and " + str(exercise.easy_points) + " points were added to your score"
                        info += " in the subject " + str(subject)

                        subject_connection.points += exercise.easy_points
                        subject_connection.save()
                        connection.completed_easy = True
                        connection.save()
                    else:
                        info += "You answered correct! But no points were added because you have answered correct to this task before!"
                else:
                    info+= "Wrong answer... try again"
                context['info'] = info
                return test(request, context)

        # LOGIC FOR CHECKING THE MEDIUM ANSWER
        elif 'medium' in request.POST:
            form = MediumAnswer(request.POST or None)
            if form.is_valid():
                question = exercise.medium_question
                context['question'] = question
                context['form'] = form
                answer = form.cleaned_data['your_answer']
                context['answer'] = answer
                answerlist = answer.split(' ')
                medium_answer_list = exercise.medium_answer.split(' ')

                if set(medium_answer_list).issubset(set(answerlist)):
                    if connection.completed_medium == False:
                        info += "You answered correct, and " + str(exercise.medium_points) + " points were added to your score"
                        info += " in the subject " + str(subject)

                        subject_connection.points += exercise.medium_points
                        subject_connection.save()
                        connection.completed_medium = True
                        connection.save()
                    else:
                        info += "You answered correct! But no points were added because you have answered correct to this task before!"
                else:
                    info+= "Wrong answer... try again"
                context['info'] = info
                return test(request, context)

        # LOGIC FOR CHECKING THE HARD ANSWER
        elif 'hard' in request.POST:
            form = HardAnswer(request.POST or None)
            if form.is_valid():
                question = exercise.hard_question
                context['question'] = question
                context['form'] = form
                answer = form.cleaned_data['your_answer']
                context['answer'] = answer
                answerlist = answer.split(' ')
                hard_answer_list = exercise.hard_answer.split(' ')

                if set(hard_answer_list).issubset(set(answerlist)):
                    if connection.completed_hard == False:
                        info += "You answered correct, and " + str(exercise.hard_points) + " points were added to your score"
                        info += " in the subject " + str(subject)
                        subject_connection.points += exercise.hard_points
                        subject_connection.save()
                        connection.completed_hard = True
                        connection.save()
                    else:
                        info += "You answered correct! But no points were added because you have answered correct to this task before!"
                else:
                    info+= "Wrong answer... try again"
                context['info'] = info
                return test(request, context)
    return render(request, 'my_subjects/exercise_page.html', context)

def test(request, context):
    return render(request, 'my_subjects/answered_task.html', context)
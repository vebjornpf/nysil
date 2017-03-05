from django.shortcuts import render, get_object_or_404

# Create your views here.
from main.models import Subject, Chapter, Exercise_Page
from .forms import EasyAnswer, MediumAnswer, HardAnswer

# this view is the "header" for the subject-pages
# its the same as main/header.html but has a sidebare too
def subject_view(req, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk) # the subject that was chosen
    # need a reference to subjects so they show up in the "Mine Fag"-dropdown menu
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/subject_header.html',{'subject_list': subjects,'subject':subject})


# this view shows alle det exercise_pages that have been added to a specific chapter
def all_exercises_view(req,chapter_pk, subject_pk):
    chapter = Chapter.objects.get(pk=chapter_pk)
    subject = Subject.objects.get(pk=chapter.subject.pk)
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/chapter_page.html', {'subject_list': subjects,'chapter':chapter,
                                                         'subject':subject})



# every time the user has submitted an answer the exercise_view will be called
# cleaned_data is a method that gives us the value to the attributes we use
    # without cleaned data: ditt_svar = <input id="id_ditt_svar" name="ditt_svar" type="text" value="2" required />
    # with cleande data: ditt_svar = 2
def exercise_view(request,chapter_pk, subject_pk, exercise_pk):
    exercise = get_object_or_404(Exercise_Page, pk=exercise_pk)
    chapter = exercise.chapter
    subject = chapter.subject
    subjects = Subject.objects.all()


    if request.method == 'POST':
        if 'easy' in request.POST:
            form = EasyAnswer(request.POST or None)
            if form.is_valid():
                print(form.cleaned_data['ditt_svar'] == exercise.easy_answer)
                # do some logic for checking the easy answer


        elif 'medium' in request.POST:
            form = MediumAnswer(request.POST or None)
            if form.is_valid():
                print(form.cleaned_data['ditt_svar'] == exercise.medium_answer)
                # do some more logic


        elif 'hard' in request.POST:
            form = HardAnswer(request.POST or None)
            if form.is_valid():
                print(form.cleaned_data['ditt_svar'] == exercise.hard_answer)
                # do some more logic

    else:
        form = EasyAnswer() # doesnt matter what type of form this is. This is just to enable the form in the questions

    return render(request, 'my_subjects/exercise_page.html', {'form': form, 'subject_list': subjects,'exercise' :exercise,'chapter':chapter,
                                                         'subject':subject})

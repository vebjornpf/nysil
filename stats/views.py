


from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render
from main.models import Subject, StudentConnectSubject, Exercise_Page, StudentConnectExercise, Chapter

def statistics_index(request):
    if not user_authenticated(request.user):
        return render(request, 'main/login.html')

    context = {'subjects': Subject.objects.all()}
    return render(request, 'stats/statistics_index.html',context)

def statistics_subject(request, subject_pk):
    context = {'subjects': Subject.objects.all(), 'subject': Subject.objects.get(pk=subject_pk)}

    return render(request, 'stats/statistics_subject.html', context)

def subject_overview(request, subject_pk):
    subject = Subject.objects.get(pk=subject_pk)
    num_students = get_number_of_students(subject)
    context = {'subjects': Subject.objects.all(), 'subject': subject, 'num_students': num_students}
    return render(request, "stats/subject_overview.html", context)


def subject_highscore(request, subject_pk):
    subject = Subject.objects.get(pk=subject_pk)

    # highscore_info on the form [[rank,connection].....[rank,connection]]
    highscore_info = fix_highscore_info(subject)

    context = {'subjects': Subject.objects.all(), 'subject': subject, 'highscore_info': highscore_info}

    return render(request, "stats/subject_highscore.html", context)

def subject_chapters(request, subject_pk):
    subject = Subject.objects.get(pk=subject_pk)

    context = {'subjects': Subject.objects.all(), 'subject': subject}

    return render(request,'stats/subject_chapters.html', context)


def subject_exercise(request, subject_pk):
    subject = Subject.objects.get(pk=subject_pk)

    context = {'subjects': Subject.objects.all(), 'subject': subject}



    return render(request, 'stats/subject_exercise.html', context)

def chapter_plot(request, subject_pk, chapter_pk):
    subject = Subject.objects.get(pk=subject_pk)
    chapter = Chapter.objects.get(pk=chapter_pk)
    info = create_chapter_graph(chapter)
    length = len(info)
    context = {'chapter': chapter, 'subjects': Subject.objects.all(), 'subject': subject, 'info': info, 'length': length}

    return render(request, 'stats/chapter_plot.html', context)


def exercise_bargraph(request, subject_pk, exercise_pk):

    exercise = Exercise_Page.objects.get(pk=exercise_pk)


    means = create_means(exercise)

    context = {'subjects': Subject.objects.all(), 'means': means, 'subject': Subject.objects.get(pk=subject_pk)}
    return render(request, 'stats/exercise_bargraph.html', context)

def subject_pie_graph(request,subject_pk):
    subject = Subject.objects.get(pk=subject_pk)
    graph_values = create_subject_graph_values(subject)

    context = {'subjects': Subject.objects.all(), 'values': graph_values , 'subject': subject}

    return render(request, 'stats/subject_graph.html', context)

# --------------------- HELP - METHODS ---------------------------

def get_number_of_students(subject):
    return StudentConnectSubject.objects.filter(subject=subject).count()

def fix_highscore_info(subject):
    info = []
    students_in_subject_conn = StudentConnectSubject.objects.filter(subject=subject).order_by('-points')
    rank=1
    max_points = get_max_points(subject)
    for student_conn in students_in_subject_conn:
        percent = (str(student_conn.points*100/max_points) if max_points > 0 else "0") + " %"
        info.append([rank, student_conn, percent])
        rank += 1
    return info

def get_max_points(subject):
    chapters = subject.chapter_set.all()
    points = 0
    for chapter in chapters:
        exercises = chapter.exercise_page_set.all()
        for exercise in exercises:
            points += exercise.easy_points + exercise.medium_points + exercise.hard_points
    return points


# see if a user is logged-in
def user_authenticated(user):
    if not user.is_authenticated():
        return False
    return True

def create_means(exercise):
    conns = StudentConnectExercise.objects.filter(exercise=exercise)
    num_of_students = conns.count()
    easy_completed = 0
    medium_completed = 0
    hard_completed = 0

    for conn in conns:
        if conn.completed_easy == True:
            easy_completed +=1
        if conn.completed_medium == True:
            medium_completed += 1
        if conn.completed_hard == True:
            hard_completed += 1
    return (easy_completed, medium_completed, hard_completed)





def create_chapter_graph(chapter):
    exercises = chapter.exercise_page_set.all()
    info = []
    counter=1
    for exercise in exercises:
        completed = 0
        connections = StudentConnectExercise.objects.filter(exercise=exercise)
        for conn in connections:
            if conn.completed_easy and conn.completed_medium and conn.completed_hard:
                completed += 1
        info.append([counter, completed])
        completed = 0
        counter += 1
    return info


# the subject-graph show how many percent all the students in a subject have completed
def create_subject_graph_values(subject):
    connections = StudentConnectSubject.objects.filter(subject=subject)
    subject_max_points = get_max_points(subject)

    # super_counter[0] -> how many students who have completed 0-9.99% percent of the subject
    # super_counter[2] -> how many students who have completed 20-29.99 percent of the subject and so on ...
    super_counter = [0 for x in range(10)]

    for connection in connections:
        percent = (connection.points / subject_max_points) * 100
        if percent <= 10:
            super_counter[0] +=1
        elif 10 < percent <= 20:
            super_counter[1] += 1
        elif 20 < percent <= 30:
            super_counter[2] += 1
        elif 30 < percent <= 40:
            super_counter[3] += 1
        elif 40 < percent <= 50:
            super_counter[4] += 1
        elif 50 < percent <= 60:
            super_counter[5] += 1
        elif 60 < percent <= 70:
            super_counter[6] += 1
        elif 70 < percent <= 80:
            super_counter[7] += 1
        elif 80 < percent <= 90:
            super_counter[8] += 1
        else:
            super_counter[9] += 1

    return super_counter
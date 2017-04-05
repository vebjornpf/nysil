import matplotlib.pyplot as plt, mpld3
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from main.models import Subject, StudentConnectSubject

def statistics_index(request):
    user_authenticated(request, request.user)

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
def user_authenticated(request,user):
    if user == AnonymousUser:
        return HttpResponseRedirect(reverse('main:login_user'))
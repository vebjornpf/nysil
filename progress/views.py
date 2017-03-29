from django.shortcuts import render
from main.models import StudentConnectSubject, StudentConnectExercise, Subject


def my_progress(request):
    user = request.user
    context = {}
    # subjects the user follows
    user_subjects = StudentConnectSubject.objects.filter(user=user)

    # the progress_overview is splitted into three columns, and we want to divide the user_subjects in theese columns
    # form of the columns = [[student_subject_connection, user_rank_in_subject, tasks_completed_percent][]..........]
    context['first_column'],  context['second_column'], context['third_column'] = set_view_context(user_subjects, user)
    return render(request, 'progress/progress_overview.html', context)


def highscore(request, subject_pk):
    user = request.user
    subject = Subject.objects.get(pk=subject_pk)
    subject_connections = StudentConnectSubject.objects.filter(subject=subject).order_by('-points')
    context = {'subject_connections': subject_connections}
    return render(request, 'progress/highscore.html', context)







# ------------------- Help-Methods ---------------------------
def set_view_context(subjects, user):
    first_subjects, second_subjects, third_subjects = split_subjects(subjects)
    first_column = []
    second_column = []
    third_column = []

    for subject in first_subjects:
        first_column.append(merge_info(subject,user))

    for subject in second_subjects:
        second_column.append(merge_info(subject, user))

    for subject in third_subjects:
        third_column.append(merge_info(subject, user))

    return first_column,second_column,third_column



def merge_info(subject_conn, user):
    user_subject_conn = StudentConnectSubject.objects.get(user=user, subject=subject_conn.subject)
    info = []

    # this adds the connection between user and subject, so we can easy get the user-score in the subject
    info.append(subject_conn)

    # adds the user-rank in the subject on the form "1 of 100"
    info.append(find_rank(subject_conn.subject, user))

    # adds how many percent of the tasks the user has completed in the subject
    divider = find_max_points(subject_conn,user)
    info.append(str((user_subject_conn.points*100)/divider) + "%" if divider>0 else "0 %")
    return info




# this method splits the subjects in to three lists
def split_subjects(subjects):
    first_column = []
    second_column = []
    last_column = []
    counter = 0
    for subject in subjects:
        if counter % 3 == 0:
            first_column.append(subject)
        elif counter % 3 == 1:
            second_column.append(subject)
        else:
            last_column.append(subject)
        counter += 1
    return first_column, second_column, last_column


# this is a help-method that finds the user rank in a spesific subject
def find_rank(subject,user):
    students_in_subject = StudentConnectSubject.objects.filter(subject=subject)
    students_in_subject = students_in_subject.order_by('-points')
    rank = 1
    for student in students_in_subject:
        if student.user == user:
            return str(rank) + " of " + str(students_in_subject.count())
        rank += 1


# this is a help-method for finding the maxium possible points a user can get in a subject
def find_max_points(subject_conn, user):
    student_exercises = StudentConnectExercise.objects.filter(user=user)
    max_points = 0

    for conn in student_exercises:
        if conn.exercise.chapter.subject == subject_conn.subject:
            max_points += conn.exercise.easy_points + conn.exercise.medium_points + conn.exercise.hard_points

    return max_points
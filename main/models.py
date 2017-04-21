from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver





class Subject(models.Model):
    subject_code = models.CharField(max_length=20, primary_key=True) # primary key
    subject_name = models.CharField(max_length=30)
    professor_firstname = models.CharField(max_length=30)
    professor_lastname = models.CharField(max_length=30)
    professor_email = models.EmailField()

    class Meta:
        ordering = ['subject_code']

    # nice when printing a Subject-object
    def __str__(self):
        return self.subject_code

    def get_full_name(self):
        return self.professor_firstname + " " + self.professor_lastname

    get_full_name.short_description = 'Professor' # headline of professor-column in the admin-table



class Chapter(models.Model):

    # order the chapter-list by chapter_number
    class Meta:
        unique_together = ('subject', 'chapter_number') # handle the exception this may cause
        ordering = ['chapter_number']

    chapter_number = models.PositiveIntegerField(default = 0)
    chapter_name = models.CharField(max_length=30)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # to controll which subject the theme belongs to


    # nice when printing a Chapter-object
    def __str__(self):
        return "Chapter " + str(self.chapter_number) + ": " + str(self.chapter_name)

    def get_number_and_name(self):
        return "Chapter" + str(self.chapter_number) + ": " + str(self.chapter_name)
    get_number_and_name.short_description = 'Chapter'



class Exercise_Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)  # to controll which chapter the exercise_page belongs to

    youtube_id = models.CharField(max_length=40)
    headline = models.CharField(max_length=30)

    # explanation describes what topics the exercises covers, so its easy to se for the students
    explanation = models.TextField(max_length=150)


    # attributes for the easy question
    easy_question = models.TextField(default='')
    easy_answer = models.CharField(max_length=30,default='')
    easy_points = models.PositiveIntegerField(default=0)

    # attributes for the medium question
    medium_question = models.TextField(default='')
    medium_answer = models.CharField(max_length=30,default='')
    medium_points = models.PositiveIntegerField(default=0)

    # attributes for the hard question
    hard_question = models.TextField(default='')
    hard_answer = models.CharField(max_length=30,default='')
    hard_points = models.PositiveIntegerField(default=0)



# a connecton between a user and a subject which controlls the points the student have in the subject
class StudentConnectSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)




# every time a student follows a subject, there is a relation between the student and all the exercises in the subject
class StudentConnectExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise_Page, on_delete=models.CASCADE)

    # theese variables controls if the student has answered correct on the questions in the exercise, so the student
    # cant answer correct all the time on the same question and gain infinity points
    completed_easy = models.BooleanField(default=False)
    completed_medium = models.BooleanField(default=False)
    completed_hard = models.BooleanField(default = False)

# ----------------------------------------------------------

# UserProfile is a model with a OneToOneField to User. This let us add fields to the nysil-user, which is importamt
# because users need to have foreign-keys to their subjects

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #test = models.IntegerField(default=5)
    subjects = models.ManyToManyField(Subject, blank=True)


    def add_subject(self, subject_pk):
        subject = Subject.objects.get(pk=subject_pk)
        student_subject_conn = StudentConnectSubject(user=self.user, subject=subject)
        find_student_subject_conn = StudentConnectSubject.objects.filter(user=self.user,subject=subject).exists()
        if not find_student_subject_conn:
            student_subject_conn.save()

        # create a StudentConnectExercise between the current student and all the exercises in the subject
        for chapter in subject.chapter_set.all():
            for exercise in chapter.exercise_page_set.all():
                connection = StudentConnectExercise(user=self.user, exercise=exercise)
                # checking for a connection between user and exercise that already exists
                find_connection = StudentConnectExercise.objects.filter(user=self.user,exercise=exercise).exists()
                if not find_connection:
                    connection.save()
        already_follows = self.subjects.filter(pk=subject_pk).exists()
        if not already_follows:

            self.subjects.add(Subject.objects.get(pk=subject_pk))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# ----------------------------------------------------------


class Comment(models.Model):
    publisher = models.ForeignKey(User)
    published_time = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    chapter = models.ForeignKey(Chapter)
    exercise = models.ForeignKey(Exercise_Page)


    def get_published_time(self):
        return str(self.published_time)[:16]


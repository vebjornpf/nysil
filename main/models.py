from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import Permission, User
=======
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# ----------------------------------------------------------

# UserProfile is a model with a OneToOneField to User. This let us add fields to the nysil-user, which is importamt
# because users need to have foreign-keys to their subjects

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    test = models.IntegerField(default=5)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# ----------------------------------------------------------
>>>>>>> master



class Subject(models.Model):
    subject_code = models.CharField(max_length=20, primary_key=True) # primary key
    subject_name = models.CharField(max_length=30)
    professor_firstname = models.CharField(max_length=30)
    professor_lastname = models.CharField(max_length=30)
    professor_email = models.EmailField()

    # nice when printing a Subject-object
    def __str__(self):
        return self.subject_code

    def get_full_name(self):
        return self.professor_firstname + " " + self.professor_lastname

    get_full_name.short_description = 'Professor' # headline of professor-column in the admin-table



class Chapter(models.Model):

    # order the chapter-list by chapter_number
    class Meta:
        unique_together = ('subject', 'chapter_number',) # TODO: handle the exception this may cause
        ordering = ['chapter_number']



    chapter_number = models.PositiveIntegerField(default = 0)
    chapter_name = models.CharField(max_length=30)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # to controll which subject the theme belongs to


    # nice when printing a Chapter-object
    def __str__(self):
        return "Kapittel " + str(self.chapter_number) + ": " + str(self.chapter_name)

    def get_number_and_name(self):
        return "Kapittel " + str(self.chapter_number) + ": " + str(self.chapter_name)
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
    easy_points = models.IntegerField(default=0)

    # attributes for the medium question
    medium_question = models.TextField(default='')
    medium_answer = models.CharField(max_length=30,default='')
    medium_points = models.IntegerField(default=0)

    # attributes for the hard question
    hard_question = models.TextField(default='')
    hard_answer = models.CharField(max_length=30,default='')
    hard_points = models.IntegerField(default=0)




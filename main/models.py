from django.db import models

# These models are the core database that control the relationships between subject, themes
# exercises, exercise pages and hints


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


class Theme(models.Model):
    chapter_number = models.IntegerField(default=0)
    chapter_name = models.CharField(max_length=30)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # to controll which subject the theme belongs to

    # nice when printing a Theme-object
    def __str__(self):
        return "Kapittel " + str(self.chapter_number) + ": " + str(self.chapter_name)

    def get_number_and_name(self):
        return "Kapittel " + str(self.chapter_number) + ": " + str(self.chapter_name)
    get_number_and_name.short_description = 'Chapter'

class Exercise_Page(models.Model):
    youtube_id = models.CharField(max_length=40)
    headline = models.CharField(max_length=30)

    # explanation describes what topics the exercises covers, so its easy to se for the students
    explanation = models.TextField(max_length=150)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE) # to controll which theme the exercise_page belongs to

    # Easy, medium and hard exercises
    easy = models.OneToOneField(Exercise, on_delete = models.CASCADE)
    medium = models.OneToOneField(Exercise, on_delete = models.CASCADE)
    hard = models.OneToOneField(Exercise, on_delete = models.CASCADE)

class Exercise(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=30) # maybe change to integer-field (?)
    points = models.IntegerField(default=0) # make test som easy_points < medium_points < hard_points






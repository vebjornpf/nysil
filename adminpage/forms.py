from django import forms
from main.models import Subject, Chapter, Exercise_Page

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code','subject_name','professor_firstname','professor_lastname','professor_email']


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ['chapter_number','chapter_name']


class ExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise_Page
        exclude = ['chapter']








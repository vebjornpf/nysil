from django import forms
from main.models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code','subject_name','professor_firstname','professor_lastname','professor_email']


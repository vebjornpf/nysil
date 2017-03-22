from django import forms
from django.contrib.auth.models import User
<<<<<<< HEAD
=======
from .models import UserProfile
>>>>>>> master

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['first_name','last_name','username', 'email', 'password']

class ProfessorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password']
=======
        fields = ['username', 'email', 'password', 'is_staff']
>>>>>>> master

from django import forms

from main.models import Exercise_Page


# ditt_svar: in english "your_answer". Use norwegian name becuase it will be displayed on the webpage
# all the classes looks the same, but doing it this way so we can separate which question the user has answered

class EasyAnswer(forms.Form):
    ditt_svar = forms.CharField()


class MediumAnswer(forms.Form):
    ditt_svar = forms.CharField()


class HardAnswer(forms.Form):
    ditt_svar = forms.CharField()
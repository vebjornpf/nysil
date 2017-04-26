from django import forms

from main.models import Comment


# ditt_svar: in english "your_answer". Use norwegian name becuase it will be displayed on the webpage
# all the classes looks the same, but doing it this way so we can separate which question the user has answered

class EasyAnswer(forms.Form):
    your_answer = forms.CharField()


class MediumAnswer(forms.Form):
    your_answer = forms.CharField()


class HardAnswer(forms.Form):
    your_answer = forms.CharField()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
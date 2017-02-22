from django.shortcuts import render, get_object_or_404

# Create your views here.
from main.models import Subject

# this view is the "header" for the subject-pages
# its the same as main/header.html but has a sidebare too
def subject_view(req, pk):
    subject = get_object_or_404(Subject, pk=pk) # the subject that was chosen
    # need a reference to subjects so they show up in the "Mine Fag"-dropdown menu
    subjects = Subject.objects.all()
    return render(req, 'my_subjects/subject_header.html',{'subject_list': subjects,'subject':subject})
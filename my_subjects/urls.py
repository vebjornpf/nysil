from django.conf.urls import url
from . import views

from main.models import Subject

app_name='my_subjects'


urlpatterns = [
    # example .../my_subjects/TDT4140
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/$', views.subject_view, name='subject_view'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/(?P<theme_pk>[A-Za-z0-9]+)/$', views.all_exercises_view, name='all_exercises_view'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/(?P<theme_pk>[A-Za-z0-9]+)/(?P<exercise_pk>[A-Za-z0-9]+)/$', views.exercise_view,
        name='exercise_view'),
]

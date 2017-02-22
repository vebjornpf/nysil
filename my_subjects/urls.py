from django.conf.urls import url
from . import views

from main.models import Subject

app_name='my_subjects'


urlpatterns = [
    # example .../my_subjects/TDT4140
    url(r'^(?P<pk>[A-Za-z0-9]+)/$', views.subject_view, name='subject_view'),
]

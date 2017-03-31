
from django.conf.urls import url
from . import views

app_name='progress'

urlpatterns = [
    url(r'^$', views.my_progress, name='my_progress'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/highscore/$', views.highscore, name='highscore'),

]

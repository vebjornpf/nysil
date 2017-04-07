from django.conf.urls import url
from . import views

app_name='stats'

urlpatterns = [
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/graph/(?P<exercise_pk>[A-Za-z0-9]+)/$', views.exercise_bargraph, name='exercise_bargraph'),
    url(r'^$', views.statistics_index, name='statistics_index'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/$', views.statistics_subject, name='statistics_subject'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/overview/$', views.subject_overview, name='subject_overview'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/highscore/$', views.subject_highscore, name='subject_highscore'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/chapters/$', views.subject_chapters, name='subject_chapters'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/exercises/$', views.subject_exercise, name='subject_exercise'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/chapter_plot/(?P<chapter_pk>[A-Za-z0-9]+)/$', views.chapter_plot, name='chapter_plot'),
    url(r'^(?P<subject_pk>[A-Za-z0-9]+)/graph/$', views.subject_pie_graph, name='subject_pie_graph'),

]

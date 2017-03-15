
from django.conf.urls import url
from . import views

app_name='adminpage'

urlpatterns = [
    url(r'^$', views.admin_index, name='admin_index'),
    url(r'^tilbakemeldinger/$',views.tilbakemeldinger, name="tilbakemeldinger"),
    url(r'^subjects/$', views.subject_overview, name='subject_overview'),
    url(r'^subjects/(?P<subject_pk>[A-Za-z0-9]+)/$', views.chapter_overview, name='chapter_overview'),
    url(r'^subjects/new_subject/$', views.new_subject, name='new_subject'),
    url(r'^subjects/(?P<subject_pk>[A-Za-z0-9]+)/new_chapter/$', views.new_chapter, name='new_chapter'),
    url(r'^subjects/(?P<subject_pk>[A-Za-z0-9]+)/delete/(?P<chapter_pk>[A-Za-z0-9]+)/$', views.delete_chapter, name='delete_chapter'),
    url(r'^subjects/(?P<subject_pk>[A-Za-z0-9]+)/delete/$', views.delete_subject, name='delete_subject'),
    url(r'^subjects/(?P<subject_pk>[A-Za-z0-9]+)/(?P<chapter_pk>[A-Za-z0-9]+)/$', views.exercise_overview,name='exercise_overview')


]

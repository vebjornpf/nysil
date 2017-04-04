
from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userregister/$', views.userregister, name='userregister'),
    url(r'^professorregister/$', views.professorregister, name='professorregister'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add_subject/(?P<subject_pk>[A-Za-z0-9]+)$', views.add_subject, name='add_subject'),
]

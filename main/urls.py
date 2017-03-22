from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main$', views.index2, name='index2'),
    url(r'^professorregister/$', views.professorregister, name='professorregister'),
    url(r'^userregister/$', views.userregister, name='userregister'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]

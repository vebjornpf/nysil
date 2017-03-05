
from django.conf.urls import url
from . import views

app_name='adminpage'

urlpatterns = [
    url(r'^$', views.admin_index, name='admin_index'),
    url(r'^subjects/$', views.subject_overview, name='subject_overview'),
    url(r'^subjects/(?P<subject_pk>[A-Za-z0-9]+)/$', views.chapter_overview, name='chapter_overview'),
    url(r'^subjects/new_subject/$', views.new_subject, name='new_subject'),

]

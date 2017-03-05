
from django.conf.urls import url
from . import views

app_name='adminpage'

urlpatterns = [
    url(r'^$', views.admin_index, name='admin_index'),
]

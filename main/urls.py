from django.conf.urls import patterns, url
from main.views import IndexView
from main import views

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^register/$', views.register, name='register'),)

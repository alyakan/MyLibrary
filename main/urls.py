from django.conf.urls import patterns, url
from main.views import IndexView
from main import views

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),)

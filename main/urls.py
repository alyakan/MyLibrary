from django.conf.urls import patterns, url
from main.views import IndexView, LibraryCreate, RegisterView
from main.views import LibraryDetail
from main import views
from django.views.generic.edit import CreateView

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^register/$', RegisterView.as_view(),
                           name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'library/add/$', LibraryCreate.as_view(),
                           name='library-add'),
                       url(r'^mylibrary/(?P<slug>[-\w]+)/$',
                           LibraryDetail.as_view(), name="library-detail"),)

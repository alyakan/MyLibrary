from django.conf.urls import patterns, url
from main.views import IndexView, LibraryCreate, RegisterView
from main.views import NotificationCreate, LoginView
from main.views import LibraryDetailView, BookCreate, LibraryListView
from main.views import BookListView, ManageBooksFormView, BookDelete
from main.views import BookDetailView, NotificationListView
from main import views

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^register/$', RegisterView.as_view(),
                           name='register'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'library/add/$', LibraryCreate.as_view(),
                           name='library-add'),
                       url(r'mylibrary/(?P<slug>[-\w]+)/book/add/$',
                           BookCreate.as_view(),
                           name='library-add'),
                       url(r'^mylibrary/(?P<slug>[-\w]+)/$',
                           LibraryDetailView.as_view(), name="library-detail"),
                       url(r'^library-list/$', LibraryListView.as_view(),
                           name='library-list'),
                       url(r'^book-list/$', BookListView.as_view(),
                           name='book-list'),
                       url(r'^mylibrary/(?P<slug>[-\w]+)/manage-books/',
                           ManageBooksFormView.as_view(),
                           name='manage-books'),
                       url(r'^mylibrary/(?P<lslug>[-\w]+)/book/(?P<slug>[-\w]+)/$',
                           BookDetailView.as_view(), name="book-detail"),
                       url(r'^mylibrary/(?P<lslug>[-\w]+)/book/(?P<slug>[-\w]+)/delete/$',
                           BookDelete.as_view(), name='book-delete'),
                       url(r'mylibrary/notification/$',
                           BookCreate.as_view(), name='notification'),
                       url(r'^notification-list/$',
                           NotificationListView.as_view(),
                           name='notification-list'),)

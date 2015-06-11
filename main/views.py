from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic import ListView, DeleteView
from main.forms import UserForm, BookForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from main.models import Library, Book
from main.models import Notification, NotificationCenter
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models.signals import post_save
import django.dispatch
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters


class PaginateMixin(object):
    paginate_by = 5


class IndexView(TemplateView):
    """
    Display the Index Page.

    Author: Aly Yakan

    **Template:**

    :template:`main/index.html`

    """
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        """
        Gets Context Data Used in main.html Template

        Author: Aly Yakan
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            current_user_id = self.request.user
            context['count'] = NotificationCenter.objects.filter(receiver_id=current_user_id, read=0).count()
            try:
                lib_id = Library.objects.get(owner_id=current_user_id).id
                context['lib_id'] = lib_id
                context['lib_slug'] = Library.objects.get(id=lib_id).slug
            except:
                lib_id = ""
            return context


class BookCreate(CreateView):
    model = Book
    # fields = ['name', 'author', 'library']
    form_class = BookForm
    success_url = reverse_lazy('index')
    template_name = 'main/book_form.html'

    def get_context_data(self, **kwargs):
        """
        Gets Context Data Used in main.html Template

        Author: Aly Yakan
        """
        context = super(BookCreate, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            current_user_id = self.request.user
            try:
                lib_id = Library.objects.get(owner_id=current_user_id).id
                context['library'] = Library.objects.get(
                    owner_id=current_user_id)
                context['lib_id'] = lib_id
                context['lib_slug'] = Library.objects.get(id=lib_id).slug
            except:
                lib_id = ""
            return context

    def send_notification(self, name):
        book_created = django.dispatch.Signal(providing_args=["id", "book_id"])
        book_created.send(sender=self.__class__, id=self.request.user.id,
                          book_id=self.object.id)


class BookListView(PaginateMixin, ListView):
    model = Book
    template_name = "main/book_list.html"
    context_object_name = "books"


class BookDetailView(DetailView):
    model = Book
    template_name = "main/book_detail.html"

    def get_context_data(self, **kwargs):
        """
        Gets Context Data Used in main.html Template

        Author: Aly Yakan
        """
        context = super(BookDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['lslug']
        library = Library.objects.get(slug=slug)
        context['library'] = library
        return context


class BookDelete(DeleteView):
    model = Book

    def get_success_url(self):
        lslug = self.kwargs['lslug']
        return reverse('library-detail', args=(lslug,))


class NotificationCreate(CreateView):
    model = Notification
    success_url = reverse_lazy('index')
    template_name = 'main/notification_form.html'

    @receiver(post_save, sender=Book)
    def my_handler(sender, instance, **kwargs):
        library = Library.objects.get(id=instance.library_id)
        actor = User.objects.get(id=library.owner_id)
        book_name = Book.objects.get(id=instance.id).name
        receivers = User.objects.exclude(id=actor.id)
        if kwargs.get('created', False):
            Notification.objects.get_or_create(verb=(library.name +
                                                     " has added a new book: " +
                                                     book_name),
                                               actor_id=actor.id,
                                               library_id=library.id,
                                               book_id=instance.id)
        pass
        notification = Notification.objects.get(verb=(library.name +
                                                      " has added a new book: " +
                                                      book_name),
                                                actor_id=actor.id,
                                                library_id=library.id,
                                                book_id=instance.id)
        for receiver in receivers:
            NotificationCenter.objects.get_or_create(receiver_id=receiver.id, notification_id=notification.id)


class NotificationListView(ListView):
    model = NotificationCenter
    template_name = "main/notification_list.html"

    def get_context_data(self, **kwargs):
        """
        Gets Context Data Used in main.html Template

        Author: Aly Yakan
        """
        context = super(NotificationListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            current_user_id = self.request.user
            try:
                object_list = NotificationCenter.objects.filter(receiver_id=current_user_id, read=0)
                context['object_list'] = object_list
                context['read_notifications'] = NotificationCenter.objects.filter(receiver_id=current_user_id)
                for obj in object_list:
                    obj.read = 1
                    obj.save()
                if object_list:
                    context['count'] = object_list.count()
                else:
                    context['count'] = 0
            except:
                lib_id = ""
            return context


class ManageBooksFormView(FormView):
    from_class = BookForm
    template_name = "main/manage_books.html"

    def post(self, request, *args, **kwargs):
        BookFormSet = modelformset_factory(Book, form=BookForm, extra=0)
        formset = BookFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('library-detail',
                                                args=(self.kwargs['slug'],)))
            pass

    def get(self, request, *args, **kwargs):
        BookFormSet = modelformset_factory(Book, form=BookForm, extra=0)
        formset = BookFormSet()
        return render_to_response('main/manage_books.html',
                                  {'formset': formset},
                                  context_instance=RequestContext(request))


class LibraryCreate(CreateView):
    model = Library
    fields = ['name', 'location', 'owner']
    success_url = reverse_lazy('index')
    template_name = 'main/library_form.html'

    # def create_book(self, name):
    #     lib_done = django.dispatch.Signal(providing_args=["id"])
    #     lib_done.send(sender=self.__class__, id=self.object.id)


class LibraryDetailView(PaginateMixin, DetailView):
    model = Library
    template = 'main/library-detail.html'

    def get_context_data(self, **kwargs):
        """
        Gets Context Data Used in library_list.html Template

        Author: Aly Yakan
        """
        context = super(LibraryDetailView, self).get_context_data(**kwargs)
        lib_slug = self.kwargs['slug']
        library = Library.objects.get(slug=lib_slug)
        context['library'] = library
        book_list = Book.objects.filter(library_id=library.id)
        paginator = Paginator(book_list, 2)
        page = self.request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        context['book_list'] = books
        context['page_obj'] = paginator.page(int(page) if page else 1)
        return context


class LibraryListView(PaginateMixin, ListView):
    model = Library
    template_name = "main/library_list.html"
    context_object_name = "libraries"


class RegisterView(FormView):
    form_class = UserForm
    template_name = 'main/register.html'
    success_url = '/main/'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, self.template_name, {'form': form,
                          'registered': registered})


# def user_login(request):

#     if request.method == 'POST':

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:

#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/main/')
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             print "Invalid login details: {0}, {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")

#     else:
#         return render(request, 'main/login.html', {})


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'

    def form_valid(self, form):
        redirect_to = self.request.GET.get('next', '')
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        l = len(redirect_to) - 1
        # return HttpResponseRedirect("/main/library_list/")
        return HttpResponse("redirect_to")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/main/')

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic import ListView
from main.forms import UserForm, BookForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from main.models import Library, Book
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext


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


# def manage_books(request):
#     BookFormSet = modelformset_factory(Book, form=BookForm)
#     QuerySet = Library.objects.filter(name='')
#     if request.method == 'POST':
#         formset = BookFormSet(request.POST, request.FILES, queryset=QuerySet)
#         if formset.is_valid():
#             formset.save()
#             return HttpResponseRedirect(reverse('book-list'))
#             pass
#     else:
#         formset = BookFormSet(queryset=QuerySet)

#     return render_to_response('manage-books.html',
#                               {'formset': formset},
#                               context_instance=RequestContext(request))


# class ManageBooksFromView(FormView):
#     from_class = modelformset_factory(Book, form=BookForm)
#     template_name = 'main/manage_books.html'


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


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'main/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/main/')

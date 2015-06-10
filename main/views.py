from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from main.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from main.models import Library
from django.core.urlresolvers import reverse_lazy


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


class LibraryCreate(CreateView):
    model = Library
    fields = ['name', 'location', 'owner']
    success_url = reverse_lazy('index')
    template_name = 'main/library_form.html'

    # def create_book(self, name):
    #     lib_done = django.dispatch.Signal(providing_args=["id"])
    #     lib_done.send(sender=self.__class__, id=self.object.id)


class LibraryDetail(DetailView):
    model = Library
    template = 'main/library-detail.html'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(LibraryDetail, self).get_context_data(**kwargs)


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

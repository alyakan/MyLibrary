from django.shortcuts import render
from django.views.generic import TemplateView
from main.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from main.models import Library
from django.core.urlresolvers import reverse_lazy


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
        if self.request.user.is_authenticated():
            current_user_id = self.request.user.id
            try:
                lib_id = Library.objects.filter(owner_id=current_user_id)
            except:
                lib_id = ""
            return {'lib_id': lib_id}


class LibraryCreate(CreateView):
    model = Library
    fields = ['name', 'location', 'owner']
    success_url = reverse_lazy('index')
    template_name = 'main/library_form.html'

    # def create_book(self, name):
    #     lib_done = django.dispatch.Signal(providing_args=["id"])
    #     lib_done.send(sender=self.__class__, id=self.object.id)


def register(request):
    """
    Registers a user to the system

    Author: Aly Yakan


    """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'main/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form, 'registered': registered})


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

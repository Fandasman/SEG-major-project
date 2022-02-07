from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import SignUpForm
from .forms import CreateClubForm
from django.conf import settings

# class LoginProhibitedMixin:
#
#      """Mixin that redirects when a user is logged in."""
#
#      redirect_when_logged_in_url = None
#
#      def dispatch(self, *args, **kwargs):
#         """Redirect when logged in, or dispatch as normal otherwise."""
#         if self.request.user.is_authenticated:
#             return self.handle_already_logged_in(*args, **kwargs)
#         return super().dispatch(*args, **kwargs)
#
#      def handle_already_logged_in(self, *args, **kwargs):
#          url = self.get_redirect_when_logged_in_url()
#          return redirect(url)
#
#      def get_redirect_when_logged_in_url(self):
#          """Returns the url to redirect to when not logged in."""
#          if self.redirect_when_logged_in_url is None:
#             raise ImproperlyConfigured(
#              "LoginProhibitedMixin requires either a value for "
#              "'redirect_when_logged_in_url', or an implementation for "
#              "'get_redirect_when_logged_in_url()'."
#              )
#          else:
#              return self.redirect_when_logged_in_url

def home(request):
    current_user = request.user
    return render(request, 'home.html')

"""This function standardize the requirements for
    user registration, if the user successfully
    registers, it will be created in the system,
    and will be redirected to the profile page """
class SignUpView(FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    #redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        pass
        #return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


"""This function standardize the requirements for
    creating clubs, if club is successfully created,
    it will be store in the database and client will
    be redirected to the home page"""
def CreateClubView(request):
    if request.method == "POST":
        form = CreateClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CreateClubForm()
    return render(request, 'create_club.html', {'form': form})

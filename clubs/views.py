from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LogInForm
from django.contrib import messages
from django.contrib.auth import login
from django.conf import settings
from .forms import SignUpForm
from django.views.generic.edit import FormView



class LoginProhibitedMixin:

     """Mixin that redirects when a user is logged in."""

     redirect_when_logged_in_url = None

     def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

     def handle_already_logged_in(self, *args, **kwargs):
         pass
        # url = self.get_redirect_when_logged_in_url()
         # url = ''
         # return redirect(url)

     def get_redirect_when_logged_in_url(self):
         pass
         # """Returns the url to redirect to when not logged in."""
         # if self.redirect_when_logged_in_url is None:
         #    raise ImproperlyConfigured(
         #     "LoginProhibitedMixin requires either a value for "
         #     "'redirect_when_logged_in_url', or an implementation for "
         #     "'get_redirect_when_logged_in_url()'."
         #     )
         # else:
         #     return self.redirect_when_logged_in_url




class LogInView(LoginProhibitedMixin,View):
    """Log-in handling view"""
    def get(self,request):
        self.next = request.GET.get('next') or 'officer'
        return self.render()

    def post(self,request):
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or 'officer'
        user = form.get_user()
        if user is not None:
                """Redirect to club selection page, with option to create new club"""
                login(request, user)
                return redirect('club_selection')

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next' : self.next})


# Create your views here.
class SignUpView(FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    #redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        #login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        pass
        #return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


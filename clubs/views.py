from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LogInForm
from django.contrib import messages
from django.contrib.auth import login




class LoginProhibitedMixin:

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('club_selection')

        return super().dispatch(*args, **kwargs)

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

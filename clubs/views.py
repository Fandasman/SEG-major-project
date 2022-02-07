from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps
from .forms import EditProfileForm
from clubs.models import User


@login_required
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('feed')
    else:
        form = EditProfileForm(instance=current_user)
    return render(request, 'edit_profile.html', {'form': form, 'user': current_user})

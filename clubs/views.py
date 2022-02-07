from django.shortcuts import redirect, render
from .forms import LogInForm
from django.contrib import messages
from django.contrib.auth import login,authenticate






def log_in(request):
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password = password)
            if user is not None:
                login(request,user)
                return redirect('log_in')
        form = LogInForm()
        return render(request, 'log_in.html', {'form':form})

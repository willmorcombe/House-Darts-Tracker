from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .decorators import login_required

import json
# Create your views here.



def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        if password == settings.SITE_PASSWORD:
            request.session['username'] = '18c'
            return redirect('/')

        # add error message
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
    return render(request, 'games/login.html')

@login_required
def logout(request):
    request.session['username'] = None
    return redirect('/login')
@login_required
def home(request):
    return render(request, 'games/home.html')

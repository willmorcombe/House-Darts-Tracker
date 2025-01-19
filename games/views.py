from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .decorators import login_required

import json
# Create your views here.
"""
Auth views
#? can maybe put this in an auth app, but its too simple and didn't seem necessary
"""

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

"""
Main app views
"""

@login_required
def home(request):
    return render(request, 'games/home.html')

def play_game(request):
    game_setup = True

    if request.method == 'GET':
        return render(request, 'games/play_game.html', context={'game_setup': game_setup})
    
    elif request.method == 'POST':
        game_setup = False
        return render(request, 'games/play_game.html', context={'game_setup': game_setup})

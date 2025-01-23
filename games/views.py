from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

from .decorators import login_required
from .api_calls import get_all_players, get_player, add_player, add_game
from .models import Player
import requests
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
Main app template views
"""

@login_required
def home(request):
    return render(request, 'games/home.html')

@login_required
def play_game(request):
    game_setup = True

    if request.method == 'GET':
        players = get_all_players(base_url= request.build_absolute_uri('/'), cookies = request.COOKIES)
        return render(request, 'games/play_game.html', context={'game_setup': game_setup, 'players' : players})
    
    elif request.method == 'POST':
        game_setup = False

        add_game_response = add_game(base_url=request.build_absolute_uri('/'), data=request.POST, cookies=request.COOKIES)
      
        if add_game_response.status_code == 201:

            game_data = add_game_response.json()
            game_data['player_one'] = get_player(
                base_url=request.build_absolute_uri('/'),
                cookies=request.COOKIES,
                pk = game_data['players'][0]
            )
            game_data['player_two'] = get_player(
                base_url=request.build_absolute_uri('/'),
                cookies=request.COOKIES,
                pk = game_data['players'][1]
            )
            return render(request, 'games/play_game.html', context={'game_setup': game_setup, 'game_data' :game_data})
        
        else:
            response_text = add_game_response.json()
            messages.error(request, response_text)
            return redirect('/play_game')
    
@login_required
def player_dashboard(request):
    if request.method == 'GET':
        # get request from a function 
        players = get_all_players(base_url= request.build_absolute_uri('/'), cookies = request.COOKIES)

        return render(request, 'games/player_dashboard.html', {'players' : players})
    
    if request.method == 'POST': # add player
        response = add_player(base_url = request.build_absolute_uri('/'), cookies=request.COOKIES, data=request.POST)
    
        if response.status_code == 201:
            return redirect('/player_dashboard')
        elif response.status_code == 400:
            response_text = response.json()['name'][0]
            messages.error(request, response_text)
            return redirect('/player_dashboard')
from django.urls import reverse
from rest_framework.response import Response

from .models import Player, Game
import requests

from typing import List

"""
All player calls
"""
def get_all_players(base_url, cookies) -> List[Player]:
    """
    A call to internal api to get all players
    """
    api_url = reverse('api/get_players')

    player_response = requests.get(url=base_url + api_url, cookies=cookies) # need to send the cookies to authenticate the user
    if player_response.status_code == 200:
        players = player_response.json()
    else:
        players = []
    return players

def get_player(base_url, cookies, pk) -> Player:
    """
    A call to internal apit to get one player
    """
    api_url = reverse('api/get_player', args=[pk])
    player_response = requests.get(url=base_url + api_url, cookies=cookies) # need to send the cookies to authenticate the user
    if player_response.status_code == 200:
        player = player_response.json()
    else:
        player = []
    return player


def add_player(base_url, cookies, data) -> Response:
    """
    A post request to add player to database
    """
    api_url = reverse('api/add_player')  # This will give you the URL path, e.g., '/api/players/'
    return requests.post(url=base_url + api_url, cookies=cookies, data=data)

"""
All game calls
"""

def get_all_games(base_url, cookies) -> List[Game]:
    """
    A call to internal api to get all games
    """
    api_url = reverse('api/get_games')

    game_response = requests.get(url=base_url + api_url, cookies=cookies) # need to send the cookies to authenticate the user
    if game_response.status_code == 200:
        games = game_response.json()
    else:
        games = []
    return games

def add_game(base_url, cookies, data) -> Response:
    """
    A post request to add a game to the database
    return: A DRF response object
    """
    api_url = reverse('api/add_game')
    return requests.post(url=base_url + api_url, cookies=cookies, data=data)
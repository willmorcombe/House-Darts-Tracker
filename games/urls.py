from django.urls import path

from . import views

urlpatterns = [
    # Main stats pages
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('play_game', views.play_game, name='play_game'),
    path('player_dashboard', views.player_dashboard, name='player_dashboard'),
    path('previous_games', views.previous_games, name='previous_games'),
    path('game_stats/<int:pk>', views.game_stats, name='game_stats'),
]

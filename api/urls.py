from django.urls import path

from . import views

urlpatterns = [
    # Main stats pages
    path('add_player', views.PlayerAPIView.as_view(), name='api/add_player'),
    path('delete_player/<int:pk>/', views.PlayerAPIView.as_view(), name='api/delete_player'), 
    path('get_players', views.PlayerAPIView.as_view(), name='api/get_players'),
    path('get_players/<int:pk>', views.PlayerAPIView.as_view(), name='api/get_player'),

    path('add_game', views.GameAPIView.as_view(), name='api/add_game'),
    path('delete_game/<int:pk>/', views.GameAPIView.as_view(), name='api/delete_game'),
    path('update_game/<int:pk>', views.GameAPIView.as_view(), name='api/update_game'),
    path('get_game', views.GameAPIView.as_view(), name='api/get_games'),
    path('get_game/<int:pk>', views.GameAPIView.as_view(), name='api/get_game'),

    path('add_leg', views.LegAPIView.as_view(), name='api/add_leg'), 
    path('get_leg', views.LegAPIView.as_view(), name='api/get_legs'),
    path('get_leg/<int:pk>', views.LegAPIView.as_view(), name='api/get_leg'),

    path('add_game_stats', views.GameStatistics.as_view(), name='api/add_game_stats'),

    path('get_checkoutlist/<int:score>', views.CheckoutListAPIView.as_view(), name='api/get_checkoutlist'),
    
]

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
]

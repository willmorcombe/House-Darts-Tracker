from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PlayerSerializer, GameSerializer

from games.decorators import login_required
from games.models import Player, Game

# Create your views here.
"""
Player API's
"""
class PlayerAPIView(APIView):
        
        @method_decorator(login_required)
        def get(self, request, pk=None, *args, **kwargs):
            if pk: # if individual player
                try:
                    player = Player.objects.get(pk=pk)
                    serializer = PlayerSerializer(player, many=False)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Player.DoesNotExist:
                    return Response({"details": 'Player not found'}, status.HTTP_404_NOT_FOUND)

            else: # if all players
                players = Player.objects.all()
                serializer = PlayerSerializer(players, many=True)
                return Response(serializer.data, status = status.HTTP_200_OK)
    
        @method_decorator(login_required)
        def post(self, request, *args, **kwargs):
            serializer = PlayerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Save the new player
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respond with the player data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        @method_decorator(login_required)
        def delete(self, request, pk, *args, **kwargs):
            try:
                player = Player.objects.get(pk=pk)  # Retrieve player by ID
                player.delete()  # Delete the player from the database
                return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content status
            except Player.DoesNotExist:
                return Response({"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND) 

"""
Game API's
"""
class GameAPIView(APIView):
     
    method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # Extracting player data from request
        player_one_id = request.data.get('player1')
        player_two_id = request.data.get('player2')
        
        if not player_one_id or not player_two_id:
            return Response({"detail": "Player IDs are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            player_one = Player.objects.get(pk=player_one_id)
            player_two = Player.objects.get(pk=player_two_id)
        except Player.DoesNotExist:
            return Response({"detail": "One or more players not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Gather additional game data
        game_data = {
            'game_type': request.data.get('game_type'),
            'best_of_legs': request.data.get('best_of_legs'),
            'best_of_sets': request.data.get('best_of_sets'),
            'players': [player_one.id, player_two.id],  # ManyToMany field requires a list of player IDs
            'completed': False  # Assuming the game is not completed when created
        }
        print(game_data)
        serializer = GameSerializer(data=game_data)
        if serializer.is_valid():
            serializer.save()  # Save the new game
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    method_decorator(login_required)
    def delete(self, request, pk, *args, **kwargs):
        try:
            game = Game.objects.get(pk=pk)  # Retrieve game by ID
            game.delete()  # Delete the game from the database
            return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content status
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND) 


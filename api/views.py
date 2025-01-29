from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PlayerSerializer, GameSerializer, CheckoutListSerializer, GameStatisticsSerializer,\
                         LegSerializer, LegStatisticsSerializer

from games.decorators import login_required
from games.models import Player, Game, CheckoutList, Leg, LegStatistics

import json

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

    @method_decorator(login_required)
    def get(self, request, pk=None, *args, **kwargs):
        if pk: # if individual game
            try:
                game = Game.objects.get(pk=pk)
                serializer = GameSerializer(game, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Game.DoesNotExist:
                return Response({"details": 'Game not found'}, status.HTTP_404_NOT_FOUND)

        else: # if all games
            completed = request.query_params.get('completed', False) # if user asked for completed games
            if completed:
                games = Game.objects.filter(completed=completed).all()
            else:
                games = Game.objects.all()

            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
     
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
            'completed': False,  # Assuming the game is not completed when created,
            
        }

        serializer = GameSerializer(data=game_data)
        if serializer.is_valid():
            serializer.save()  # Save the new game
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    method_decorator(login_required)
    def patch(self, request, pk, *args, **kwargs):
        """
        Used as an object update to create winner and change game status
        """
        try:
            game = Game.objects.get(pk=pk)  # Retrieve the game by ID
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # get winner
        winner_id = int(request.data.get("winner"))
        
        try:
            winner = Player.objects.get(pk=winner_id)
        except Player.DoesNotExist:
            return Response({"detail": "Winner player not found."}, status=status.HTTP_404_NOT_FOUND)
        
        game_data = {
            'winner': winner_id,
            'completed': True,
            'raw_game_data' : json.loads(request.data.get('raw_game_data'))
        }

        serializer = GameSerializer(game, data=game_data, partial=True)  # Use partial=True to update only specified fields
        if serializer.is_valid():
            serializer.save()  # Save the updated game data
            # here, create a new game statics object for each player in the game and 
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    method_decorator(login_required)
    def delete(self, request, pk, *args, **kwargs):
        try:
            game = Game.objects.get(pk=pk)  # Retrieve game by ID
            game.delete()  # Delete the game from the database
            return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content status
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND) 


class LegAPIView(APIView):

    @method_decorator(login_required)
    def get(self, request, pk=None, *args, **kwargs):
        if pk: # if individual leg
            try:
                leg = Leg.objects.get(pk=pk)
                serializer = LegSerializer(leg, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Leg.DoesNotExist:
                return Response({"details": 'Leg not found'}, status.HTTP_404_NOT_FOUND)

        else: # if all legs
            legs = Leg.objects.all()
            serializer = LegSerializer(legs, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
     
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
        leg_data = {
            'leg_number' : request.data.get('leg_number'),
            'players': [player_one.id, player_two.id],  # ManyToMany field requires a list of player IDs
            'raw_leg_data' : json.loads(request.data.get('raw_leg_data')),
            'game' : request.data.get('game_id'),
            'winner' : request.data.get('winner'),
        }

        leg_serializer = LegSerializer(data=leg_data)
        if leg_serializer.is_valid():
            leg_serializer.save()  # Save the new leg
            # then create new leg stats data using leg_serializer is valid overwritting
            leg_serializer_data = leg_serializer.data

            for player_id in leg_serializer_data['raw_leg_data'].keys():
                leg_stats_serializer = LegStatisticsSerializer(data={
                    'leg' : leg_serializer_data['id'],
                    'player' : player_id,
                })

                if leg_stats_serializer.is_valid():
                    leg_stats_serializer.save() # Save the new leg stats data using leg_
                else: 
                    print(leg_stats_serializer.errors)
                    #todo: error log here
            return Response(leg_serializer.data, status=status.HTTP_201_CREATED)
        return Response(leg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        

class GameStatistics(APIView):
    def post(self, request, *args, **kwargs):
        game_stats_serializer = GameStatisticsSerializer(data=request.data)
        if game_stats_serializer.is_valid():
            game_stats_serializer.save()  # Save the new game
            
            return Response(game_stats_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(game_stats_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckoutListAPIView(APIView):
    @method_decorator(login_required)
    def get(self, request, score, *args, **kwargs):
        checkout_data = CheckoutList.objects.filter(score=score).first()
        serializer = CheckoutListSerializer(checkout_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)



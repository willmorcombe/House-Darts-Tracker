from rest_framework import serializers
from games.models import Player, Game

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def validate_name(self, value):
        """
        Custom function to validate whether the name is already in use
        """
        # Check if a player with this name already exists
        if Player.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"A player with the name '{value}' already exists.")
        return value


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    # def validate_players(self, value):
    #     """
    #     Custom function to validate whether there are exactly two players
    #     """
    #     # Check if a player with this name already exists
    #     if Player.objects.filter(name=value).exists():
    #         raise serializers.ValidationError(f"A player with the name '{value}' already exists.")
    #     return value
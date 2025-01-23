from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Player(models.Model):
    """
    Table contents: Contains data about a player
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Override str rep
        """
        return self.name

class GameStateHistory(models.Model):
    """
    Table contents: Contains ALL data about a specific game that was played
    """
    raw_game_data = models.TextField()

class Game(models.Model):
    """
    Table contents: Contains metadata about a game thats been played
    """
    id = models.BigAutoField(primary_key=True)
    game_date = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(max_length=20)
    best_of_legs = models.IntegerField()
    best_of_sets = models.IntegerField()
    players = models.ManyToManyField(Player, related_name='games')
    completed = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_games')  # The winner of the game (can be null if the game isn't finished yet)

    def clean(self):
        """ Custom validation to ensure there are only 2 players in the game """
        if self.players.count() != 2:
            raise ValidationError('A game must have 2 players.')
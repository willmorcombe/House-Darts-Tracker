from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Player(models.Model):
    """
    Table contents: Contains data about a player
    """
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Override str rep
        """
        return self.name


class Game(models.Model):
    """
    Table contents: Contains metadata about a game that's been played
    """
    id = models.BigAutoField(primary_key=True)
    game_date = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(max_length=20)
    best_of_legs = models.IntegerField()
    best_of_sets = models.IntegerField()
    players = models.ManyToManyField(Player, related_name='games')
    completed = models.BooleanField(default=False)
    raw_game_data = models.JSONField(null=True)
    winner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_games')  # The winner of the game (can be null if the game isn't finished yet)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game on {self.game_date} ({self.game_type})"


class GameStatistics(models.Model):
    """
    Table contents: Contains statistics for each player in a specific game
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    three_dart_avg = models.FloatField(default=0.0)
    first_nine_avg = models.FloatField(default=0.0)
    checkout_rate = models.FloatField(default=0.0)
    best_dart_leg = models.IntegerField(default=0)
    legs_won = models.IntegerField(default=0)  
    sets_won = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Stats for {self.player.name} in game {self.game.id}"

class Leg(models.Model):
    """
    Table contents: Contains metadata about a leg of a game
    """
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='legs')  # One-to-many relationship with Game
    players = models.ManyToManyField(Player, related_name='legs')
    raw_leg_data = models.JSONField(null=False)
    leg_number = models.IntegerField(null=False)
    winner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_legs')  # The winner of the leg (can be null if the leg isn't finished yet)

    def __str__(self):
        return f"Leg {self.id} of Game {self.game.id}"
    

class LegStatistics(models.Model):
    """
    Table contents: Contains statistics for each leg in a specific game
    """
    leg = models.ForeignKey(Leg, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    number_of_throws = models.IntegerField(default=0)
    three_dart_avg = models.FloatField(default=0.0)
    first_nine_avg = models.FloatField(default=0.0)
    checkout_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"Leg {self.leg_number} in game {self.game.id}"


class CheckoutList(models.Model): 
    id = models.AutoField(primary_key=True)
    score = models.IntegerField() 
    dart_one = models.CharField(null=True, max_length=5)
    dart_two = models.CharField(null=True, max_length=5)
    dart_three = models.CharField(null=True, max_length=5)

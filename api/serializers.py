from rest_framework import serializers
from games.models import Player, Game, CheckoutList, GameStatistics, LegStatistics, Leg
from api.lib.GameStatsCalculator import LegStatsCalculator, GameStatsCalculator

class PlayerSerializer(serializers.ModelSerializer):
    """
    Making only full name required in input, first and last name should only be returned in outputing the
    object, not as input.
    """
    full_name = serializers.CharField(required=True)  # Ensure full_name is required
    first_name = serializers.CharField(read_only=True)  # Make first_name read-only
    last_name = serializers.CharField(read_only=True)   # Make last_name read-only

    class Meta:
        model = Player
        fields = '__all__'

    def validate_full_name(self, value):
        """
        Custom function to validate whether the name is already in use
        """
        # Check if a player with this name already exists
        if Player.objects.filter(full_name=value).exists():
            raise serializers.ValidationError(f"A player with the name '{value}' already exists.")
        return value
    
    def create(self, validated_data):
        """
        Overwrite the create player method, to get the validated data, add first_name and last_name
        to the validated data and then call the super
        """
        # Compute first_name and last_name from full_name
        full_name = validated_data.get("full_name")
        name_parts = full_name.split()
        validated_data["first_name"] = name_parts[0]
        validated_data["last_name"] = " ".join(name_parts[1:])  # Handle middle names if present
        return super().create(validated_data)


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'

    def to_representation(self, instance):
        """
        Override to_representation method (which builds the dictionary from the object) 
        to ensure that when serializing for GET requests,
        the winner field is serialized as a full Player object instead of just an ID.
        """
        representation = super().to_representation(instance)

        # If the winner is not null, replace the winner ID with the full Player data
        if instance.winner:
            # Use the PlayerSerializer to serialize the winner field
            winner_serializer = PlayerSerializer(instance.winner)
            representation['winner'] = winner_serializer.data

        return representation


class LegSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leg
        fields = '__all__'

    def to_representation(self, instance):
        """
        Override to_representation method (which builds the dictionary from the object) 
        to ensure that when serializing for GET requests,
        the winner field is serialized as a full Player object instead of just an ID.
        """
        representation = super().to_representation(instance)

        # If the winner is not null, replace the winner ID with the full Player data
        if instance.winner:
            # Use the PlayerSerializer to serialize the winner field
            winner_serializer = PlayerSerializer(instance.winner)
            representation['winner'] = winner_serializer.data

        return representation

class LegStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegStatistics
        fields = '__all__'

    def is_valid(self):
        """
        Override the create object to also create the stats based off of the raw_data field.
        """
        leg_obj_id = self.initial_data['leg']
        player_obj_id = self.initial_data['player']
        raw_leg_data = Leg.objects.get(pk=leg_obj_id).raw_leg_data[player_obj_id]
        stats_calc = LegStatsCalculator(raw_leg_data)
        self.initial_data.update(stats_calc.get_stats())
        
        return super().is_valid()

class GameStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameStatistics
        fields = '__all__'


    def create(self, validated_data):
        """
        Override the is valid object to also create the stats based off of the raw_data field.
        """
        
        return super().create(validated_data)

class CheckoutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutList
        fields = '__all__'

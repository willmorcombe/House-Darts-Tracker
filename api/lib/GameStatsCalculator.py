import statistics

class LegStatsCalculator:
    """
    Used to calculate leg stats from one leg of a game
    """
    def __init__(self, raw_leg_data: dict):
        self.raw_leg_data = raw_leg_data['raw_leg_score']
        self.darts_on_checkout = raw_leg_data['darts_used_on_checkout']


    def __calculate_number_of_throws(self) -> float:
        return len(self.raw_leg_data) * 3
    
    def __calculate_first_nine_avg(self) -> float:
        return round(statistics.mean([self.raw_leg_data[i-1] - self.raw_leg_data[i] for i in range(1, len(self.raw_leg_data))][:3]), 2)
    
    def __calculate_three_dart_avg(self) -> float:
        return round(statistics.mean([self.raw_leg_data[i-1] - self.raw_leg_data[i] for i in range(1, len(self.raw_leg_data))]), 2)
    
    def __calculate_checkout_rate(self) -> float:
        return round(self.darts_on_checkout / (len(self.raw_leg_data) * 3), 4) * 100


    def get_stats(self):
        # Return the full set of stats in a dictionary
        return {
            'number_of_throws': self.__calculate_number_of_throws(),
            'three_dart_avg': self.__calculate_three_dart_avg(),
            'first_nine_avg': self.__calculate_first_nine_avg(),
            'checkout_rate': self.__calculate_checkout_rate(),
        }


class GameStatsCalculator:
    def __init__(self):
        # turn into list of lists for each leg played
        # all_legs = []
        # total_checkout_attempts = 0
        # for k, v in raw_game_data.items():
        #     all_legs.append(v[player_id]['raw_leg_score'])
        #     total_checkout_attempts += v[player_id]['darts_used_on_checkout'] 
        # self.raw_game_data = all_legs
        # self.total_checkout_attempts = total_checkout_attempts
        pass

    def __calculate_three_dart_avg(self):
        # Implement logic to calculate 3-dart average based on raw_game_data
        # return statistics.mean([   round(statistics.mean([l[i-1] - l[i] for i in range(1, len(l))]), 2) for l in self.raw_leg_data   ])
        return 0
    def __calculate_first_nine_avg(self):
        # Implement logic to calculate first 9 darts average based on raw_game_data
        return 0.0  # Placeholder logic, replace with actual calculation

    def __calculate_checkout_rate(self):
        # Implement logic to calculate checkout rate based on raw_game_data
        return 0.0  # Placeholder logic, replace with actual calculation

    def __calculate_best_dart_leg(self):
        # Implement logic to calculate best dart leg based on raw_game_data
        return 0  # Placeholder logic, replace with actual calculation

    def __calculate_legs_won(self):
        # Implement logic to calculate legs won based on raw_game_data
        return 0  # Placeholder logic, replace with actual calculation

    def __calculate_sets_won(self):
        # Implement logic to calculate sets won based on raw_game_data
        return 0  # Placeholder logic, replace with actual calculation

    def get_stats(self):
        # Return the full set of stats in a dictionary
        return {
            'three_dart_avg': self.__calculate_three_dart_avg(),
            'first_nine_avg': self.__calculate_first_nine_avg(),
            'checkout_rate': self.__calculate_checkout_rate(),
            'best_dart_leg': self.__calculate_best_dart_leg(),
            'legs_won': self.__calculate_legs_won(),
            'sets_won': self.__calculate_sets_won(),
        }
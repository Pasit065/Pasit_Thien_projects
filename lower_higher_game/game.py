
import random

class Game():
    def __init__(self):
        self.maximum_attempt = {}
        self.correct_numbers = random.randint(0, 100)
        self.mode = None
        self.turn = 1

    def set_next_turn(self):
        self.turn += 1
        
    # def set_maximum_attempt(self):
    def ask_player_name(self):
        return input("What is your nickname: ")

    def display_winners_text(self, players_name):
        winners_text = f"Congraduation!!!. {players_name} have won this game.\nCorrect answer is {self.correct_numbers}"
        print(winners_text)
    
    def get_initial_lifes(self, all_modes_data):
        return all_modes_data[self.mode]["lifes"]

    def set_mode(self, all_modes_data):
        self.mode = input("Which mode do you want to plays (easy, medium, hard): ")
        if self.mode not in all_modes_data:
            raise ValueError(f"You have choose {self.mode} mode. But it not availables.")


    def display_rules(self):
        rules_text = """Welcome to highers lowers games!!!.
              With 'easy' mode you have 10 lifes to guess numbers.
              With 'medium' mode you have 7 lifes to guess numbers.
              With 'hard' mode you have 3 lifes to guess numbers.\n"""
        
        print(rules_text)

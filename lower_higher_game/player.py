class Player():
    def __init__(self, id, player_mode, remain_lifes, name):
        self.id = id
        self.mode = player_mode
        self.remain_lifes = remain_lifes
        self.name = name
        self.guess_numbers = None

    def set_guess_numbers(self, turn):
        player_ans = int(input(f"This is {turn} turn.\nGuess numbers: "))
        self.guess_numbers = {
            "turn":turn,
            "answer":player_ans
        }



class LifesManagers():
    def __init__(self):
        self.player_records = []

    def get_decreased_lifes(self, remain_lifes):
        return remain_lifes - 1

    def is_alive(self, players_lifes):
        if players_lifes > 0:
            return True
        elif players_lifes == 0:
            return False
        else:
            raise ValueError("It seems your life is negative. Please check your program again.")



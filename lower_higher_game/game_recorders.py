import pandas

class GameRecorders():
    def __init__(self):
        self.json_players_records = None
        self.database_players_records = {}

    def set_json_players_records(self, json_players_records):
        self.json_players_records = json_players_records

    def display_current_players_records(self):
        df = pandas.DataFrame(self.json_players_records)

        print(df)


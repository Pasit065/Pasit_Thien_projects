import json
import sqlite3

class DataService():
    def __init__(self, json_records_points_path):
        self.json_records_points_path = json_records_points_path
        self.db_table_name_list = ["players"]
        self.db_all_data = {}

    def get_json_records_data(self):
        with open(self.json_records_points_path, 'r') as file:
            return file.read()
        
    def update_json_records_data(self, new_data):
        if type(new_data) != dict:
            raise ValueError("Your records data type is not compatible to our json files.")
         
        with open(self.json_records_points_path, 'w') as file:
            json.dump(new_data, file, indent=len(new_data))

    def get_json_players_format_data(self, players_cols, all_players_rows):
        data_dict = {col:[] for col in players_cols}

        for row in all_players_rows:
            data_dict['id'].append(row[0])
            data_dict['name'].append(row[1])
            data_dict['mode'].append(row[2])
            
            if row[3]:
                data_dict['is_win'].append(True)
            else:
                data_dict['is_win'].append(False)

        return data_dict




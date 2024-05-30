import random
import pprint
from player import Player
from lifes_managers import LifesManagers
from data_service import DataService
from game import Game
from game_recorders import GameRecorders
import sqlite3
import os
import pathlib
import datetime as dt
import json
import pandas

def insert_new_row_to_answers_table(table_name, id, name, mode, guess, time_spending):
    insert_new_row_query = f'''
        INSERT INTO {table_name}(id, name, mode, guess, time)
        VALUES ({id}, "{name}", "{mode}", {guess}, "{str(time_spending)}")
        '''
    
    curr.execute(insert_new_row_query)
    conn.commit()

def insert_new_players_data(id, name, mode, is_win):
    insert_new_row_query = f'''
        INSERT INTO players(id, name, mode, is_win)
        VALUES ({id}, '{name}', '{mode}', {is_win})
        '''
    
    curr.execute(insert_new_row_query)
    conn.commit()

def calculate_spending_times(initial_time, now):
    return now - initial_time

def set_working_path(working_path):
    os.chdir(working_path)

def wrong_answers_text_display(status, remian_lifes):
    print(f"Incorrect!!!. Your answers is {status} than correct answers. \nAnd you have {remian_lifes} lifes left.\n")

def get_all_rows_datas(table_name, curr):
    select_all_row = f'''
    SELECT *
    FROM {table_name}'''

    curr.execute(select_all_row)
    return curr.fetchall()

ALL_MODES_DATA = {
    "easy":{"lifes":10}, 
    "medium":{"lifes":7}, 
    "hard":{"lifes":3}
    }

PARRENT_PATH = str(pathlib.Path(__file__).parent.resolve())
working_path = PARRENT_PATH 
json_records_path = working_path + '/game_record_data.json'

set_working_path(working_path = working_path)

game_recorders = GameRecorders()
lifes_managers = LifesManagers()
game = Game()

# get Json initial records data.
data_service = DataService(json_records_points_path = json_records_path)
    
# Connect to new database.
conn = sqlite3.connect('./game_records.db')
curr = conn.cursor()

for table_name in data_service.db_table_name_list:
    if table_name == "players":
        create_table_if_not_exist = f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
        id integers primary key,
        name varchar(255) unique,
        mode varchar(255),
        is_win boolean
        )'''

        select_all_row = f'''
        SELECT *
        FROM {table_name}'''

        curr.execute(create_table_if_not_exist)
        conn.commit()

        game_recorders.database_players_records[table_name] = get_all_rows_datas(table_name = table_name, curr = curr)
        conn.commit()

# Initialize 'game' and 'player' data
def runing_game():
    current_id = len(game_recorders.database_players_records["players"])
    answers_table_name = f"answers_{current_id}"

    conn = sqlite3.connect('./game_records.db')
    curr = conn.cursor()

    create_answers_table_for_new_player = f'''
        CREATE TABLE IF NOT EXISTS {answers_table_name}(
        id integers,
        name varchar(255),
        mode varchar(255),
        guess integers,
        time varchar(255)
        )'''
    
    curr.execute(create_answers_table_for_new_player)
    conn.commit()
    

    game.display_rules()
    game.set_mode(all_modes_data = ALL_MODES_DATA)

    player_modes = game.get_initial_lifes(all_modes_data = ALL_MODES_DATA)
    player_name = game.ask_player_name()

    player = Player(id = current_id, player_mode = game.mode, remain_lifes = player_modes, name = player_name)

    while True:
        initial_time = dt.datetime.now()
        player.set_guess_numbers(turn = game.turn)

        if player.guess_numbers["answer"] == game.correct_numbers:
            game.display_winners_text(players_name = player.name)
            is_win = True
            break
        elif player.guess_numbers["answer"] > game.correct_numbers:
            wrong_answers_text_display(status = "greater", remian_lifes = player.remain_lifes)
        elif player.guess_numbers["answer"] < game.correct_numbers:
            wrong_answers_text_display(status = "lower", remian_lifes = player.remain_lifes)
    
        player.remain_lifes = lifes_managers.get_decreased_lifes(remain_lifes = player.remain_lifes)
        is_alive = lifes_managers.is_alive(players_lifes = player.remain_lifes)
        time_spending = calculate_spending_times(initial_time = initial_time, now = dt.datetime.now())
        
        insert_new_row_to_answers_table(answers_table_name, current_id, player_name, game.mode, player.guess_numbers["answer"], time_spending.seconds)

        if is_alive:
            game.set_next_turn()
        else:
            print(f"Unfortunetly. You have lose this game correct answers is {game.correct_numbers}")
            is_win = False
            break

    
    insert_new_players_data(id=current_id, name = player.name, mode = game.mode, is_win = is_win)

    select_all_players_row = f'''
        SELECT *
        FROM players'''
    
    curr.execute(select_all_players_row)

    game_recorders.database_players_records['players'] = curr.fetchall()
    all_rows_data = game_recorders.database_players_records['players'] 

    conn.commit()

    curr = conn.execute('SELECT * FROM players')
    all_players_column = [col[0] for col in curr.description]

    data_dict = data_service.get_json_players_format_data(all_players_column, all_rows_data)

    game_recorders.set_json_players_records(data_dict)
    data_service.update_json_records_data(new_data = game_recorders.json_players_records)

    game_recorders.display_current_players_records()

    



    



runing_game()
conn.close()

# tables = ['players', 'answers_0']
# all_tables_data = {}

# conn = sqlite3.connect('./game_records.db')
# # cur = conn.execute('SELECT * FROM answers_0')
# cur = conn.cursor()
# query = '''
#     SELECT name
#     FROM sqlite_master
    
#     WHERE type = 'table'
#     '''

# cur.execute(query)
# all_tables = [table[0] for table in cur.fetchall()]

# conn.commit()

# for table in all_tables:
#     cur = conn.execute(f'SELECT * FROM {table}')

#     all_tables_data[table] = {'columns':[col[0] for col in cur.description]}
#     conn.commit()


# cur = conn.cursor()

# for table in all_tables_data:
#     query = f'''
#         SELECT * 
#         FROM {table}
#         '''
    
#     cur.execute(query)
#     all_tables_data[table]['data'] = cur.fetchall()

#     if all_tables_data[table]['data'] and len(all_tables_data[table]['columns']) != len(all_tables_data[table]['data'][0]):
#         raise ValueError(f"Total of column is not the same as total column of data in table {table}")

# new_tables = all_tables_data['players']
# data_dict = {col:[] for col in new_tables['columns']}

# for row in new_tables['data']:
#     data_dict['id'].append(row[0])
#     data_dict['name'].append(row[1])
#     data_dict['mode'].append(row[2])

#     if row[3]:
#         data_dict['is_win'].append(True)
#     else:
#         data_dict['is_win'].append(False)

# df = pandas.DataFrame(data_dict)
# pprint.pprint(df)
# # players_cols = ["id", "name", "mode", "is_win"]
# # answers_cols = ["id", "name", "answer", "total_spending_time_(s)"]

# # def get_each_table_dataframe(all_col, table_data):
# #     all_rows_data = {col:[] for col in all_col}

# #     for row in table_data
    
# conn.close()
    
    



        












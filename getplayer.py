import nba_api.stats.static.players as static_players
import nba_api.stats.static.teams as static_teams
import nba_api.stats.endpoints.commonplayerinfo as commonplayerinfo
import random
import pandas as pd
from datetime import datetime, date

def get_active_player():
    # returns a random dictionary "player"
    # helper function to initialize a player
    players = static_players.get_active_players()
    player = random.choice(players)
    return player


def get_player_id(player): 
    # returns ID of a player so we can retrieve their stats/info
    # helper function for get_player_info
    return player['id']

def get_player_info(player):
    # takes a player dictionary and returns a pandas view of their information
    # helper function to get a player's information
    p_id = get_player_id(player)
    player = commonplayerinfo.CommonPlayerInfo(player_id=p_id).common_player_info.get_data_frame().iloc[0]
    return player

def initialize_player():
    # initialize a random player.
    player = get_active_player()
    player_info = get_player_info(player)
    return player_info

player = initialize_player()

def get_age(player):
    # takes a birthdate string and a datetime object and returns the age as a string
    bday = player.loc['BIRTHDATE']
    today = datetime.now()
    bday_str = str(bday).strip()
    if "T" in bday_str:
        bday_str = bday_str.split("T", 1)[0]

    birth_date = datetime.strptime(bday_str, "%Y-%m-%d").date()
    today_date = today.date() if isinstance(today, datetime) else today

    age = today_date.year - birth_date.year
    if (today_date.month, today_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return int(age)

# print(player['DISPLAY_FIRST_LAST'])
# print(player['POSITION'])
# print(get_age(player))


class Player:
    def __init__(self):
        self.name = None
        self.age = None
        self.position = None
        self.height = None
        self.team = None
        self.jersey = None
        self.id = None
        self.set_random_player()

    def __str__(self):
        return f"Player: {self.name}, Age: {self.age}, Position: {self.position}, Height: {self.height}, Team: {self.team}, Jersey: {self.jersey}"
    
    def set_info(self, player):
        # helper function to set info
        self.id = player.loc['PERSON_ID']
        self.name = player.loc['DISPLAY_FIRST_LAST']
        self.age = get_age(player)
        self.position = player.loc['POSITION']
        self.height = player.loc['HEIGHT']
        self.team = player.loc['TEAM_ABBREVIATION']
        self.jersey = player.loc['JERSEY']

    def set_random_player(self):
        player = initialize_player()
        self.set_info(player)
        print("Random player set.")


player = Player()
print(player)
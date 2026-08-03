import nba_api.stats.static.players as static_players
import nba_api.stats.static.teams as static_teams
import nba_api.stats.endpoints.commonplayerinfo as commonplayerinfo
import nba_api.stats.endpoints.teaminfocommon as teaminfocommon
import random
import pandas as pd
from datetime import datetime, date

def get_random_active_player():
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
    player = get_random_active_player()
    player_info = get_player_info(player)
    return player_info
    

def get_age(player):
    # takes a birthdate string and a datetime object and returns the age as an integer
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


def get_height_in_inches(height):
    # convert a height string like "6-10" into total inches for easy comparison
    if not height:
        return None

    if isinstance(height, (int, float)):
        return int(height)

    parts = str(height).strip().split("-")
    if len(parts) != 2:
        return None

    feet, inches = parts
    return int(feet) * 12 + int(inches)


def format_height_in_feet_inches(total_inches):
    # convert total inches back to a display string like "6-10"
    if total_inches is None:
        return None

    feet = total_inches // 12
    inches = total_inches % 12
    return f"{feet}-{inches}"

# TEAM CLASS
class Team:

    def __init__(self, id):
        # because we will only initialize a team object when we are setting up a player,
        # we will initialize the team with the provided ID
        try:
            # attempt to get team info from api, id comes from player.set_info() 
            # then generate team object
            df = teaminfocommon.TeamInfoCommon(team_id=id).get_data_frames()
            df = df[0]
            df = df.iloc[0]
            self.name = df.loc['TEAM_NAME']
            self.conference = df.loc['TEAM_CONFERENCE']
            self.division = df.loc['TEAM_DIVISION']
            self.id = df.loc['TEAM_ID']
            self.abbreviation = df.loc['TEAM_ABBREVIATION']
        except Exception:
            # exception if a player is not currently rostered on a team. 
            # if a player is not rostered on a team i plan to just get another player. work around for now
            static_team = next(
                (team for team in static_teams.get_teams() if team.get('id') == id),
                None,
            )
            if static_team is None:
                self.name = "Unknown"
                self.conference = None
                self.division = None
                self.id = id
                self.abbreviation = "UNK"
            else:
                self.name = static_team['full_name']
                self.conference = static_team.get('conference')
                self.division = static_team.get('division')
                self.id = static_team['id']
                self.abbreviation = static_team['abbreviation']

# PLAYER CLASS
class Player:
    def __init__(self):
        # initialize empty player
        self.name = None
        self.age = None
        self.position = None
        self.height = None
        self.team = None
        self.jersey = None
        self.id = None

    def __str__(self):
        return f"Player: {self.name}, Age: {self.age}, Position: {self.position}, Height: {format_height_in_feet_inches(self.height)}, Team: {self.team.abbreviation}, Jersey: {self.jersey}"

    def print(self):
        print(self)

    def set_player_by_name(self, name):
        player = static_players.find_players_by_full_name(name)
        if len(player) == 1:
            player = player[0]
            player = get_player_info(player)
            self.set_info(player)
        elif len(player) > 1:
            print("Multiple players found with that name.")
        else:
            print("Player not found.")


    def set_info(self, player):
        # set player info, takes player dictionary and updates player object
        # we will initialize team with team object that is passed a team ID
        self.id = player.loc['PERSON_ID']
        self.name = player.loc['DISPLAY_FIRST_LAST']
        self.age = get_age(player)
        self.position = player.loc['POSITION']
        self.height = get_height_in_inches(player.loc['HEIGHT'])
        self.team = Team(player.loc['TEAM_ID'])
        self.jersey = player.loc['JERSEY']

        if len(self.team.name) == 0: # if team name is not set, get a new player
            self.set_random_player()
        if len(self.jersey) == 0: # if no jersey number, get a new player
            self.set_random_player()

    def set_random_player(self):
        player = initialize_player()
        self.set_info(player)

# comparison functions
def compare_position(p1, p2):
    # compare positions of two players, return string describing difference
    # we will find the index of player position and use difference to find distance
    positions = ["Guard", "Guard-Forward", "Forward-Guard", "Forward", "Forward-Center", "Center-Forward", "Center"]
    pos1 = positions.index(p1.position)
    pos2 = positions.index(p2.position)
    diff = pos1 - pos2
    if diff == 0:
        return "position ="
    elif diff == 1 or diff == -1:
        return "position close"
    else:
        return "wrong position"

def compare_height(p1, p2):
    h1 = p1.height
    h2 = p2.height

    diff = h1 - h2
    if diff == 0:
        return "height ="
    elif diff > 0 and diff < 3:
        return "height +"
    elif diff < 0 and diff > -3:
        return "height -"
    elif diff > 3:
        return "height ++"
    else:
        return "height --"

def compare_age(p1, p2):
    a1 = p1.age
    a2 = p2.age

    diff = a1 - a2
    if diff == 0:
        return "age ="
    elif diff > 0 and diff < 3:
        return "age +"
    elif diff < 0 and diff > -3:
        return "age -"
    elif diff > 3:
        return "age ++"
    else:
        return "age --"

def compare_jersey(p1, p2):
    j1 = int(p1.jersey)
    j2 = int(p2.jersey)

    # edge case for a player's jersey is "00"
    if p1.jersey == "00":
        j1 = -1
    if p2.jersey == "00":
        j2 = -1

    diff = j1 - j2
    if diff == 0:
        return "jersey ="
    elif diff > 0 and diff < 4:
        return "jersey +"
    elif diff < 0 and diff > -4:
        return "jersey -"
    elif diff > 3:
        return "jersey ++"
    else:
        return "jersey --"


if __name__ == "__main__":
    player = Player()
    player.set_player_by_name("Jayson Tatum")
    player.print()

    player2 = Player()
    player2.set_player_by_name("Jordan Clarkson")
    player2.print()

    print(compare_position(player, player2))
    print(compare_height(player, player2))
    print(compare_age(player, player2))
    print(compare_jersey(player, player2))

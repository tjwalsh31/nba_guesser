"""NBA player helper utilities for random player selection and comparison."""

import random
from datetime import datetime
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats, teaminfocommon
from nba_api.stats.static import players as static_players
from nba_api.stats.static import teams as static_teams
from requests.exceptions import RequestException


def get_random_active_player():
    """Return a random active player dictionary."""
    players = static_players.get_active_players()
    return random.choice(players)


def get_player_id(player_data):
    """Return the NBA player ID from an active player record."""
    return player_data["id"]


def get_player_info(player_data):
    """Return a pandas Series containing information for the given player."""
    p_id = get_player_id(player_data)

    try:
        player_info = (
            commonplayerinfo.CommonPlayerInfo(player_id=p_id)
            .common_player_info
            .get_data_frame()
            .iloc[0]
        )
    except (RequestException, ValueError, IndexError, KeyError):
        fallback_data = {
            "PERSON_ID": p_id,
            "DISPLAY_FIRST_LAST": (
                player_data.get("full_name")
                or player_data.get("name")
                or "Unknown Player"
            ),
            "BIRTHDATE": None,
            "POSITION": None,
            "HEIGHT": None,
            "TEAM_ID": None,
            "TEAM_ABBREVIATION": None,
            "JERSEY": None,
        }
        player_info = pd.Series(fallback_data)

    return player_info


def initialize_player():
    """Initialize a random active player and return their info series."""
    player_data = get_random_active_player()
    return get_player_info(player_data)


def get_age(player_info):
    """Calculate the age of a player based on their birthdate."""
    bday = player_info.loc["BIRTHDATE"]
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
    """Convert a height string like "6-10" into total inches."""
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
    """Format total inches into a feet-inches display string."""
    if total_inches is None:
        return None

    feet = total_inches // 12
    inches = total_inches % 12
    return f"{feet}-{inches}"

def get_active_players_by_full_name(name):
    """Return a list of active players matching the given full name."""
    active_players = static_players.get_active_players()
    matched_players = []
    for player in active_players:
        if name.lower() in player["full_name"].lower():
            matched_players.append(player)
    return matched_players



class Team:
    """Represents a team with metadata from the NBA API or static team list."""

    def __init__(self, team_id):
        if team_id is None:
            self.name = "Unknown"
            self.conference = None
            self.division = None
            self.id = None
            self.abbreviation = "UNK"
            return

        try:
            df = teaminfocommon.TeamInfoCommon(team_id=team_id).get_data_frames()[0]
            df = df.iloc[0]
            self.name = df.loc["TEAM_NAME"]
            self.conference = df.loc["TEAM_CONFERENCE"]
            self.division = df.loc["TEAM_DIVISION"]
            self.id = df.loc["TEAM_ID"]
            self.abbreviation = df.loc["TEAM_ABBREVIATION"]
        except (RequestException, ValueError, IndexError, KeyError):
            static_team = next(
                (team for team in static_teams.get_teams() if team.get("id") == team_id),
                None,
            )
            if static_team is None:
                self.name = "Unknown"
                self.conference = None
                self.division = None
                self.id = team_id
                self.abbreviation = "UNK"
            else:
                self.name = static_team["full_name"]
                self.conference = None
                self.division = None
                self.id = static_team["id"]
                self.abbreviation = static_team["abbreviation"]


class Player:  # pylint: disable=too-many-instance-attributes
    """Represents an NBA player and their current metadata."""

    def __init__(self):
        self.name = None
        self.age = None
        self.position = None
        self.height = None
        self.current_team = None
        self.jersey = None
        self.id = None
        self.all_teams = None
        self.target = False
        self.debug = False
        self.set_random_player()


    def __str__(self):
        return (
            f"Player: {self.name}, Age: {self.age}, Position: {self.position}, "
            f"Height: {format_height_in_feet_inches(self.height)}, "
            f"Team: {self.current_team.abbreviation}, Jersey: {self.jersey}"
        )


    def print(self):
        """Print the player representation."""
        print(self)


    def toggle_debug(self):
        """Toggle debug mode on the player."""
        self.debug = not self.debug
        print(f"Debug mode is now {self.debug}")


    def set_all_teams(self):
        """Populate all teams the player has played for."""
        player_career_stats = (
            playercareerstats.PlayerCareerStats(player_id=self.id).get_data_frames()[0]
        )
        past_teams = player_career_stats["TEAM_ABBREVIATION"].unique()

        if self.current_team.abbreviation not in past_teams:
            past_teams = np.append(past_teams, self.current_team.abbreviation)
        if "TOT" in past_teams:
            past_teams = np.delete(past_teams, np.where(past_teams == "TOT"))
        if "UNK" in past_teams:
            past_teams = np.delete(past_teams, np.where(past_teams == "UNK"))

        self.all_teams = past_teams
        return past_teams


    def set_player_by_name(self, name):
        """Load player info by full name."""
        matched_players = get_active_players_by_full_name(name)
        if len(matched_players) == 1:
            player_info = get_player_info(matched_players[0])
            print(player_info)
            self.set_info(player_info)

        elif len(matched_players) > 1:
            print("Multiple players found with that name.")
            idx = 0

            for player in matched_players:
                print(f"{idx}:  ", player["full_name"])
                idx += 1
            found = False
            while(not found):
                try:
                    choice = int(input("Enter number of player you want to select: "))
                    if 0 <= choice < len(matched_players):
                        player_info = get_player_info(matched_players[choice])
                        self.set_info(player_info)
                        found = True
                        break
                    else:
                        print("Invalid choice. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        
        else:
            print("Player not found.")


    def set_info(self, player_info):
        """Update the player object from player information."""
        if self.debug:
            print()

        self.id = player_info.loc["PERSON_ID"]
        self.name = player_info.loc["DISPLAY_FIRST_LAST"]
        self.age = get_age(player_info)
        self.position = player_info.loc["POSITION"]
        self.height = get_height_in_inches(player_info.loc["HEIGHT"])
        self.current_team = Team(player_info.loc["TEAM_ID"])
        self.jersey = player_info.loc["JERSEY"]
        if self.target:
            self.all_teams = self.set_all_teams()

        if len(self.current_team.name) == 0:
            self.set_random_player()
        if len(self.jersey) == 0:
            self.set_random_player()


    def set_random_player(self):
        """Load a random active player into this Player object."""
        player_info = initialize_player()
        self.set_info(player_info)


    def set_target(self):
        self.target = True
        self.set_all_teams()


p1 = Player()
p1.set_player_by_name("Steph")
p1.print()
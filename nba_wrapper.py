from nba_api.stats.static import players as static_players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats, teaminfocommon
from requests.exceptions import RequestException
import pandas as pd




def get_player_id(player_dict):
    return player_dict["id"]

def get_fallback_data(p_id, player_dict):
    """Helper function to make API_Wrapper class much cleaner"""
    fallback_data = {
        "PERSON_ID": p_id,
        "DISPLAY_FIRST_LAST": (
            player_dict.get("full_name")
            or player_dict.get("name")
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



"""This class is an NBA_API Wrapper to separate api calls from other functions. """

class NBAApiClient:

    def get_active_players(self):
        players = static_players.get_active_players()
        return players


    def get_player_by_id(self, player_id):
        return static_players.find_player_by_id(player_id)


    def get_player_info(self, player_dict):
        """Return a pandas Series containing information for the given player."""
        p_id = get_player_id(player_dict)
        try:
            player_info = (
                commonplayerinfo.CommonPlayerInfo(player_id=p_id)
                .common_player_info
                .get_data_frame()
                .iloc[0]
            )
        except (RequestException, ValueError, IndexError, KeyError):
            player_info = get_fallback_data(p_id, player_dict)
        return player_info

    def search_players_by_name(self, name):
        return static_players.find_players_by_full_name(name)

    def get_team_info(self, team_id):
        try:
            team_info = teaminfocommon.TeamInfoCommon(team_id=team_id).team_info_common.get_data_frame().iloc[0]
        except (RequestException, ValueError, IndexError, KeyError):
            team_info = {
                "TEAM_ID": team_id,
                "TEAM_ABBREVIATION": "UNK",
                "TEAM_NAME": "Unknown Team",
                "TEAM_CONFERENCE": None,
                "TEAM_DIVISION": None,
            }
        return team_info

    def get_career_stats(self, player_id):
        return playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]


    
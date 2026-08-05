import nba_api.stats.static.players as static_players
import nba_api.stats.static.teams as static_teams
import nba_api.stats.endpoints.commonplayerinfo as commonplayerinfo
import nba_api.stats.endpoints.teaminfocommon as teaminfocommon
import nba_api.stats.endpoints.playercareerstats as playercareerstats
import random
import pandas as pd
from getplayer import *



player = static_players.find_players_by_full_name("LeBron James")[0]
player_info = get_player_info(player)

# print(player_info)
print(player_info['DISPLAY_FIRST_LAST'])
p_id = player_info['PERSON_ID']

player_career_stats = playercareerstats.PlayerCareerStats(player_id=p_id).get_data_frames()[0]
print(player_career_stats)
# teams_played_for = player_career_stats['TEAM_ABBREVIATION'].unique()


# print(random_player)

# print(teams)
# print(team_abrv)

def main():
    pass

if __name__ == "__main__":
    main()

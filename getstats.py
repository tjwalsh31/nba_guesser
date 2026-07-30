from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
import random
import pandas as pd

all_players = players.get_active_players()
# print(all_players)
rand_player = random.choice(all_players)
# print(rand_player["full_name"])

player_info = commonplayerinfo.CommonPlayerInfo(player_id=rand_player["id"])
df = player_info.get_data_frames()[0]

# print(df.columns)
print(df.iloc[0])
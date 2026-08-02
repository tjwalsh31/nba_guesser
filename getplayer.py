from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
import random
import pandas as pd
import datetime


def get_info():
    d = {}
    player = random.choice(players.get_active_players())
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player["id"])
    df= player_info.get_data_frames()[0]
    
    d["Name"] = df.loc[0, "DISPLAY_FIRST_LAST"]
    d["Position"] = df.loc[0, "POSITION"]
    d["Height"] = df.loc[0, "HEIGHT"]
    d["Jersey"] = df.loc[0, "JERSEY"]
    d["Team"] = df.loc[0, "TEAM_ABBREVIATION"]
    d["Age"] = df.loc[0, "BIRTHDATE"]
    d["Age"] = datetime.datetime.now().year - int(d["Age"].split("-")[0])
    return d

# print(get_info())

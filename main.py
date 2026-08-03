import nba_api.stats.static.players as static_players
import nba_api.stats.static.teams as static_teams
import nba_api.stats.endpoints.commonplayerinfo as commonplayerinfo
import nba_api.stats.endpoints.teaminfocommon as teaminfocommon
import pandas as pd


teams = static_teams.get_teams()
team_dict = {}
for team in teams:
    team_dict[team['abbreviation']] = team['id']
# print(team_dict)
df = teaminfocommon.TeamInfoCommon(team_id=team_dict['LAL']).get_data_frames()
df = df[0]
df = df.iloc[0]
print(df)
# print(teams)
# print(team_abrv)

def main():
    pass

if __name__ == "__main__":
    main()

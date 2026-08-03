import nba_api.stats.static.players as static_players
import nba_api.stats.static.teams as static_teams
import nba_api.stats.endpoints.commonplayerinfo as commonplayerinfo


teams = static_teams.get_teams()
team_abrv = []
for team in teams:
    team_abrv.append(team['abbreviation'])

print(team_abrv)

def main():
    pass

if __name__ == "__main__":
    main()

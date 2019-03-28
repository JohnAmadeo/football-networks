import json

players = {}

with open('dutch-players.json', 'r') as f:
    team_players = json.load(f)
    for team in team_players:
        players[team] = team_players[team]

with open('english-players.json', 'r') as f:
    team_players = json.load(f)
    for team in team_players:
        players[team] = team_players[team]

with open('french-players.json', 'r') as f:
    team_players = json.load(f)
    for team in team_players:
        players[team] = team_players[team]

with open('german-players.json', 'r') as f:
    team_players = json.load(f)
    for team in team_players:
        players[team] = team_players[team]

with open('italian-players.json', 'r') as f:
    team_players = json.load(f)
    for team in team_players:
        players[team] = team_players[team]

with open('players.json', 'w') as f:
    json.dump(players, f)
from bs4 import BeautifulSoup
import requests
import json

def get_players(team=None, year=None):
    # scrape players across all teams and years
    if team == None and year == None:
        teams = get_team_ids()
        print('Checkpoint: Done getting team ids')
        players = {}
        for team in teams:
            team_players = get_players(team=team)
            players[team] = team_players
            print('Checkpoint: Done getting players from ' + team)
        
        return players

    # scrape a team's players across all year
    elif team != None and year == None:
        players = {}

        for year in range(2019, 1949, -1):
            player, success = get_players(team, year)
            if not success:
                break
            players[year] = player
            print('Checkpoint: Done getting ' + team + ' players from ' + str(year))

        return players 

    # error state 
    elif team == None and year != None:
        return Exception('Cannot specify a year if team is not specified')

    # scrape the player for a particular team and year
    else: 
        resp = requests.get('https://www.worldfootball.net/teams/' + team + '/' + str(year) + '/2/')
        if resp.status_code != 200:
            return [], False

        html = BeautifulSoup(resp.content, 'html.parser')

        positions = ['Goalkeeper', 'Midfielder', 'Defender', 'Forward']
        player_table = None
        for table in html.find_all(class_='standard_tabelle'):
            if len(table.find_all(string=positions)) > 0:
                player_table = table
                break

        if player_table == None:
            return [], True

        player = []
        for tr in player_table.find_all('tr'):
            if len(tr.find_all(string=['Coach', 'Manager'])) > 0:
                break
            if len(tr.find_all('td')) == 0:
                continue

            player.append(tr.find_all('td')[2].string)

        return player, True

def get_team_ids():
    # Top 2 leagues in England, Italy, Germany, and Span
    # Top league in France, Netherlands
    league_urls = [
        'https://www.worldfootball.net/players/eng-premier-league-2018-2019/',
        'https://www.worldfootball.net/players/eng-championship-2018-2019/',
        'https://www.worldfootball.net/players/bundesliga-2018-2019/',
        'https://www.worldfootball.net/players/2-bundesliga-2018-2019/',
        'https://www.worldfootball.net/players/fra-ligue-1-2018-2019/',
        'https://www.worldfootball.net/players/ita-serie-a-2018-2019/',
        'https://www.worldfootball.net/players/ita-serie-b-2018-2019/',
        'https://www.worldfootball.net/players/esp-primera-division-2018-2019/',
        'https://www.worldfootball.net/players/esp-segunda-division-2018-2019/',
        'https://www.worldfootball.net/players/ned-eredivisie-2018-2019/'
    ]

    team_ids = []
    for url in league_urls:
        resp = requests.get(url)
        html = BeautifulSoup(resp.content, 'html.parser')
        
        teams_table = None
        for table in html.find_all(class_='standard_tabelle'):
            if len(table.find_all(string=['player', 'Matches'])) > 0:
                teams_table = table
                break

        for tr in teams_table.find_all('tr'):
            url = tr.find_all('td')[1].a['href']
            team_ids.append(url.split('/')[2])
        
    return team_ids


players = get_players()
with open('players.json', 'w') as f:       
    json.dump(players, f)

from bs4 import BeautifulSoup
import requests
import json
from multiprocessing import Pool

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

def get_teams_in_league(league_url):
    team_ids = []
    resp = requests.get(league_url)
    html = BeautifulSoup(resp.content, 'html.parser')
    
    teams_table = None
    for table in html.find_all(class_='standard_tabelle'):
        if len(table.find_all(string=['player', 'Matches'])) > 0:
            teams_table = table
            break

    for tr in teams_table.find_all('tr'):
        league_url = tr.find_all('td')[1].a['href']
        team_ids.append(league_url.split('/')[2])
        
    return team_ids

def get_squads_in_league(league_url):
    teams = get_teams_in_league(league_url)
    league_squads = {}
    for team in teams:
        league_squads[team] = get_squads_in_team(team)

    league_name = league_url_to_name(league_url)
    with open(league_name + '-players.json', 'w') as f:
        json.dump(league_squads, f)
        pass

def get_squads_in_team(team):
    team_squads = {}

    for year in range(2019, 1949, -1):
        player, success = get_squad_in_team_and_year(team, year)
        if not success:
            break
        team_squads[year] = player
        print('Checkpoint: Done getting ' +
              team + ' players from ' + str(year))

    return team_squads

def get_squad_in_team_and_year(team, year):
    resp = requests.get(
        'https://www.worldfootball.net/teams/' + team + '/' + str(year) + '/2/')
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

    players = []
    for tr in player_table.find_all('tr'):
        if len(tr.find_all(string=['Coach', 'Manager'])) > 0:
            break
        if len(tr.find_all('td')) == 0:
            continue

        players.append(tr.find_all('td')[2].string)

    return players, True

def league_url_to_name(url):
    return '-'.join(url.split('/')[-2].split('-')[:-2])

def main():
    # # Create a pool of workers
    # pool = Pool(len(league_urls))

    # # The pool will run sync with each argument
    # # spread across the workers.
    # pool.map(get_squads_in_league, league_urls)
    
    players = {}
    for url in league_urls:
        league_name = league_url_to_name(url)

        print(league_name)
        with open(league_name + '-players.json', 'r') as f:
            team_players = json.load(f)
            players[league_name] = {}
            for team in team_players:
                players[league_name][team] = team_players[team]

    with open('players.json', 'w') as f:
        json.dump(players, f)

main()

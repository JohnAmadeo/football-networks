from bs4 import BeautifulSoup
import requests

resp = requests.get('https://www.worldfootball.net/teams/manchester-united/2019/2/')
html = BeautifulSoup(resp.content, 'html.parser')

player_table = []
for table in html.find_all(class_='standard_tabelle'):
    if len(table.find_all(string='Midfielder')) > 0:
        player_table = table

players = []
for tr in player_table.find_all('tr'):
    if len(tr.find_all(string=['Coach', 'Manager'])) > 0:
        break
    if len(tr.find_all('td')) == 0:
        continue

    players.append(tr.find_all('td')[2].string)

print(players)
        

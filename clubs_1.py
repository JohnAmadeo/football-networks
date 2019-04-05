'''
Graph structure:
Nodes: clubs
Edges (Undirected): no. of players who played in both teams

Question:
Do clubs trade more with domestic teams vs. transnational teams?
- Player movement for a Eredivisie club (2010-2019).png
- Player movement for a La Liga club (2010-2019).png
- No. of domestic shared players vs. No. of transnational shared players (2010-2019).png

Insight:
Clubs trade domestically more than they do transnationally
'''

import csv
import json
from matplotlib import pyplot
from scipy import stats

LEAGUES = set([
    'eng-premier-league',
    # 'eng-championship',
    'bundesliga',
    # '2-bundesliga',
    'fra-ligue-1',
    'ita-serie-a',
    # 'ita-serie-b',
    'esp-primera-division',
    # 'esp-segunda-division',
    'ned-eredivisie'
])

def get_edges(data):
    edges = []
    team_players = {}
    for league in data.keys():
        if league not in LEAGUES:
            continue

        for team in data[league].keys():
            team_players[team] = set()
            for year in range(2019, 2009, -1):
                squad = data[league][team][str(year)]
                team_players[team].update(squad)

    teams = sorted(team_players.keys())
    for team_a in teams:
        for team_b in teams:
            if team_a == team_b:
                continue

            shared_players = team_players[team_a].intersection(
                team_players[team_b])
            edges.append({
                'source': team_a,
                'target': team_b,
                'weight': len(shared_players),
                'type': 'Undirected',
            })

    for edge in edges:
        print(edge['source'] + ' & ' + edge['target'] +
              ' : ' + str(edge['weight']))

    return edges

def get_nodes(data):
    nodes = []
    for league in data.keys():
        if league not in LEAGUES:
            continue

        for team in data[league].keys():
            nodes.append({
                'id': team,
                'label': team,
                'league': league
            })

    return nodes 

def save_edges_as_csv(edges):
    with open('clubs_1_edges.csv', 'w') as f:
        writer = csv.writer(f)

        labels = ['Source', 'Target', 'Weight', 'Type']
        rows = [[edge['source'], edge['target'], edge['weight'], edge['type']]
                for edge in edges]
        writer.writerow(labels)
        writer.writerows(rows)

def save_nodes_as_csv(nodes):
    with open('clubs_1_nodes.csv', 'w') as f:
        writer = csv.writer(f)

        labels = ['Id', 'Label', 'League']
        rows = [[node['id'], node['label'], node['league']] for node in nodes]
        writer.writerow(labels)
        writer.writerows(rows)

'''
Question: Is player movement within a country larger than across countries?
Output: 
a. 2D scatter plot of no. of domestic shared players vs. transnational ones
b. 2D scatter plot of domestic shared players / team vs. transnational shared players / team
'''
def validate(data, node, edges):
    teams_in_league = {}
    team_to_league = {}
    for league in data.keys():
        teams_in_league[league] = set(data[league].keys())
        for team in data[league].keys():
            team_to_league[team] = league
    
    shared_players = {}
    for edge in edges:
        source = edge['source']
        target = edge['target']

        if source not in shared_players:
            shared_players[source] = {'domestic': 0, 'transnational': 0}

        if team_to_league[source] == team_to_league[target]:
            shared_players[source]['domestic'] += edge['weight']
        else:
            shared_players[source]['transnational'] += edge['weight']

    x = []
    y = []
    for team in shared_players.keys():
        x.append(shared_players[team]['transnational'])
        y.append(shared_players[team]['domestic'])

    max_val = max([max(x), max(y)])
    pyplot.scatter(x, y)
    pyplot.plot(range(max_val), range(max_val))
    pyplot.xlim(xmin=0, xmax=max_val)
    pyplot.ylim(ymin=0, ymax=max_val)
    pyplot.xlabel('No. of players shared with transnational clubs')
    pyplot.ylabel('No. of players shared with domestic clubs')
    pyplot.show()

def main():
    with open('players.json', 'r') as f:
        data = json.load(f)

    nodes = get_nodes(data)
    edges = get_edges(data)

    save_nodes_as_csv(nodes)
    save_edges_as_csv(edges)

    validate(data, nodes, edges)

main()

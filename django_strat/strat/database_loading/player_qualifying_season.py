import csv

import requests
from bs4 import BeautifulSoup as bs


def load_file():
    with open('available_players.csv') as csvfile:
        file = csv.reader(csvfile)
        players = []
        for row in file:
            players.append(row)
    return players


def save_file(save_info):
    with open('players.csv', 'w') as csvffile:
        csvwrite = csv.writer(csvffile)
        for row in save_info:
            csvwrite.writerow(row)


def get_player_url(id):
    url = "https://www.baseball-reference.com/players/{}/{}.shtml".format(id[0], id)
    return url


def get_player_page(url, player_type):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    table = soup.find_all('tbody')[0]
    rows = table.find_all('tr', class_='full')
    qualified_seasons = 0
    questionable_seasons = 0
    if player_type == 'p':
        for r in rows:
            cells = r.find_all('td')
            games_started = cells[8].get_text()
            innings_pitched = cells[13].get_text()
            games_started = int(games_started)
            innings_pitched = float(innings_pitched)
            if innings_pitched >= 40:
                qualified_seasons += 1
            elif innings_pitched >= 25:
                if games_started == 0:
                    qualified_seasons += 1
                elif games_started <= 2:
                    questionable_seasons += 1
    elif player_type == 'h':
        for r in rows:
            cells = r.find_all('td')
            plate_appearances = cells[4].get_text()
            plate_appearances = int(plate_appearances)
            if plate_appearances >= 100:
                qualified_seasons += 1
    return qualified_seasons, questionable_seasons


def assign_contract(player):
    contract = ['', 0]
    if player[3] > 3:
        contract[0] = 'FA'
    elif player[3] == 3:
        if player[4] == 0:
            contract = ['Y3', 600000]
        else:
            contract[0] = 'lookup'
    elif player[3] == 2:
        if player[4] == 0:
            contract = ['Y2', 550000]
        else:
            contract[0] = 'lookup'
    elif player[3] == 1:
        if player[4] == 0:
            contract = ['Y1', 500000]
        else:
            contract[0] = 'lookup'
    elif player[3] == 0:
        if player[4] == 0:
            contract = ['AAA', 250000]
        else:
            contract[0] = 'lookup'
    return contract


def main():
    players = load_file()
    returned_players = []
    for p in players:
        p.append(get_player_url(p[0]))
        p.extend(get_player_page(p[2], p[1]))
        p.extend(assign_contract(p))
        returned_players.append(p)
        print(p)
    save_file(returned_players)



if __name__ == '__main__':
    main()
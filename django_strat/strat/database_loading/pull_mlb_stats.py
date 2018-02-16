import csv
import datetime

import requests
from bs4 import BeautifulSoup as bs


def load_players():
    players = []
    with open('players.csv', 'r') as csvfile:
        file = csv.reader(csvfile)
        for row in file:
            players.append(row)
    players.pop(0)
    return players


def get_player_url(id):
    url = "https://www.baseball-reference.com/players/{}/{}.shtml".format(id[0], id)
    return url


def get_split_url(id, year, player_type):
    if player_type.lower() == 'h':
        t = 'b'
    else:
        t = 'p'
    return 'https://www.baseball-reference.com/players/split.fcgi?id={}&year={}&t={}'.format(id, year, t)


def get_player_page(url, id, player_type):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    active_status = [id, False]
    stat_list, split_stats, war = [], [], []
    if '404 error' not in str(soup):
        war = extract_war(page, player_type)
        for w in war:
            w.insert(0, id)
        table = soup.find_all('tbody')[0]
        minor_row = table.find_all('tr', class_='minors_table')
        spacer_row = table.find_all('tr', class_='spacer')
        full_season = table.find_all('tr', class_='full')
        partial_row = table.find_all('tr', class_='partial_table')
        rows = table.find_all('tr')
        for r in rows:
            if r in partial_row and r not in spacer_row:
                start = str(r).find('csk')
                year = int(str(r)[start + 5: start + 9])
                part = int(str(r)[start +10: start + 12])
                stat_line = get_stat_line(r, year, part, id, player_type)
                stat_list.append(stat_line)
                if year >= (datetime.datetime.now().year - 2):
                    active_status[1] = True
            if r in minor_row:
                year = int(r.find_all('th')[0].get_text())
                if year >= (datetime.datetime.now().year - 2):
                    active_status[1] = True
            if r in full_season:
                start = str(r).find('standard')
                year = int(str(r)[start + 9: start + 13])
                stat_line = get_stat_line(r, year, 0, id, player_type)
                stat_list.append(stat_line)
                if year >= (datetime.datetime.now().year - 2):
                    active_status[1] = True
                if player_type == 'x':
                    split_url = get_split_url(id, year, 'h')
                    split_stats.extend(get_split_stats(split_url, id, year, 'h'))
                    split_url = get_split_url(id, year, 'p')
                    split_stats.extend(get_split_stats(split_url, id, year, 'p'))
                else:
                    split_url = get_split_url(id, year, player_type)
                    split_stats.extend(get_split_stats(split_url, id, year, player_type))
            if r in spacer_row:
                pass
            if year:
                print(year)
    return stat_list, split_stats, active_status, war


def extract_war(page, player_type):
    soup = bs(page.text, 'html.parser')
    soup = str(soup)
    cut = soup.find('<div class="placeholder">')
    soup = soup[cut:]
    soup = soup.replace('<!--', '')
    soup = soup.replace('-->', '')
    soup = bs(soup, 'html.parser')
    war_return = []
    if player_type == 'p':
        div = soup.find_all('div', id='div_pitching_value')[0]
        table = div.find_all('table')[0]
        rows = table.find_all('tr', class_='full')
        for r in rows:
            data = r.find_all(attrs={'data-stat': 'WAR_pitch'})
            data = str(data[0])
            if 'csk' in data:
                loc = data.find('csk')
                data = data[loc + 5:]
                loc = data.find('"')
                data = data[:loc]
                year = r.find_all('th')[0].get_text()
                team = r.find_all('td')[1].get_text()
                war_return.append([year, team, data])
    elif player_type == 'h':
        div = soup.find_all('div', id='div_batting_value')[0]
        table = div.find_all('table')[0]
        rows = table.find_all('tr', class_='full')
        for r in rows:
            data = r.find_all(attrs={'data-stat': 'WAR'})
            data = str(data[0])
            if 'csk' in data:
                loc = data.find('csk')
                data = data[loc + 5:]
                loc = data.find('"')
                data = data[:loc]
                year = r.find_all('th')[0].get_text()
                team = r.find_all('td')[1].get_text()
                war_return.append([year, team, data])
    return war_return


def get_stat_line(stat_row, year, part, id, player_type):
    stat_line = [id, player_type, year, part]
    stat_row = stat_row.find_all('td')
    for s in stat_row:
        stat_line.append(s.get_text())
    return stat_line


def get_split_stats(url, id, year, player_type):
    stats_list = []
    try:
        page = requests.get(url)
        soup = bs(page.text, 'html.parser')
        soup = str(soup)
        cut = soup.find('<div class="placeholder">')
        soup = soup[cut:]
        soup = soup.replace('<!--', '')
        soup = soup.replace('-->', '')
        soup = bs(soup, 'html.parser')
        table = soup.find_all('table', id='plato')[0]
        rows = table.find_all('tr')[1:]
        for r in rows:
            stat_line = [id, player_type, year]
            temp_stat_line = []
            title = r.find_all('th')[0].get_text()
            if title in ['vs RHB', 'vs LHB', 'vs LHP', 'vs RHP']:
                temp_stat_line.append(title)
                cells = r.find_all('td')
                for c in cells:
                    temp_stat_line.append(c.get_text())
                if title in ['vs LHP', 'vs RHP']:
                    temp_stat_line.pop(2)
                if len(temp_stat_line):
                    stat_line.extend(temp_stat_line)
                    stats_list.append(stat_line)
        return stats_list
    except IndexError:
        return []


def save_file(save_info, file_name):
    with open(file_name, 'a') as csvfile:
        csvwrite = csv.writer(csvfile)
        for row in save_info:
            csvwrite.writerow(row)


def main():
    players = load_players()
    player_status, full_stats, split_stats, war_list = [], [], [], []
    for p in players[2635:]:
        print(p[1], p[2], p[3])
        stats, splits, status, war = get_player_page(get_player_url(p[0]), p[0], p[3])
        if stats:
            full_stats.extend(stats)
            split_stats.extend(splits)
            war_list.extend(war)
        else:
            status[1] = True
        player_status.append(status)
    save_file(player_status, 'status.csv')
    save_file(full_stats, 'mlb_stats.csv')
    save_file(war_list, 'war_list.csv')
    save_file(split_stats, 'mlb_splits.csv')


if __name__ == '__main__':
    main()

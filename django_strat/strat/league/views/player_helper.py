from league.models.transactions import AvailableFreeAgent, AvailableDraftPick
from league.models.players import HitterCardStats, \
    Contract
from league.models.players import HitterCardStats, \
    Contract
from league.models.transactions import AvailableFreeAgent, AvailableDraftPick


def collect_team(player, year):
    team = ''
    contract = Contract.objects.filter(player=player, year=year)
    if len(contract) == 1:
        team = '{} {}'.format(contract[0].team.location, contract[0].team.nickname)
    elif len(contract) == 0:
        free_agents = AvailableFreeAgent.objects.filter(player=player, year=year)
        if len(free_agents) == 1:
            team = 'Free Agent'
        else:
            draft_picks = AvailableDraftPick.objects.filter(player=player, year=year)
            if len(draft_picks) == 1:
                team = 'Available in Draft'
    return team


def collect_player_position(player):
    position = ''
    if player.player_type == 'p':
        position += 'Pitcher, '
    if player.player_type == 'x':
        position += 'Pitcher, '
    if player.player_type in 'hx':
        cards = HitterCardStats.objects.filter(player=player)
        defensive_strings = ''
        for c in cards:
            defensive_strings += '{} '.format(c.defensive_string)
        while len(defensive_strings) > 3:
            if defensive_strings[:2] == 'c-':
                if 'Catcher' not in position:
                    position += 'Catcher, '
                defensive_strings = defensive_strings[2:]
            elif defensive_strings[:3] == '1b-':
                if 'Firstbase' not in position:
                    position += 'Firstbase, '
                defensive_strings = defensive_strings[3:]
            elif defensive_strings[:3] == '2b-':
                if 'Secondbase' not in position:
                    position += 'Secondbase, '
                defensive_strings = defensive_strings[2:]
            elif defensive_strings[:3] == '3b-':
                if 'Thirdbase' not in position:
                    position += 'Thirdbase, '
                defensive_strings = defensive_strings[2:]
            elif defensive_strings[:3] == 'ss-':
                if 'Shortstop' not in position:
                    position += 'Shortstop, '
                defensive_strings = defensive_strings[2:]
            elif defensive_strings[:3] == 'lf-':
                if 'Left Field' not in position:
                    position += 'Left Field, '
                defensive_strings = defensive_strings[2:]
            elif defensive_strings[:3] == 'cf-':
                if 'Center Field' not in position:
                    position += 'Center Field, '
                defensive_strings = defensive_strings[2:]
            elif defensive_strings[:3] == 'rf-':
                if 'Right Field' not in position:
                    position += 'Right Field, '
            else:
                defensive_strings = defensive_strings[1:]
    position = position[:-2]
    return position

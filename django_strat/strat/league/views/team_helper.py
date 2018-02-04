from django.db.models import Q

from league.models.players import Contract, HitterCardStats, PitcherCardStats
from league.models.teams import Payroll, Team
from league.models.transactions import Arbitration, DraftPick

"""
A possible team_dict keys and where they are generated:
id, team abbreviation (str), generated in collect_team or collect_teams
team, team object, generated in collect team or collect_teams
roster, roster list (of dict), generated in collect_roster
payroll, payroll dict, generated in collect_payroll
adjustment, adjustment list (of dict), generated in collect_adjustments
draft_pick, draft pick list (of dict), generated in collect_draft_pick
"""


def collect_teams(year):
    """
    Takes a year and returns a list of team dictionaries with the id and team keys
    return:
        list of dictionaries of teams
    """

    team_list = Team.objects.filter(year=year).order_by('location')
    teams = []
    for t in team_list:
        team = {
            'id': t.abbreviation,
            'team': t,
        }
        teams.append(team)
    return teams


def collect_team(year, abbreviation):
    """
    Takes a year and abbreviation and returns a team dictionary with the id and team keys
    return:
        dictionary of a team
    """

    team = Team.objects.filter(year=year, abbreviation=abbreviation)[0]
    team = {
        'id': abbreviation,
        'team': team,
    }
    return team


def collect_roster(team_dict):
    """
    Takes a team_dict and adds a roster key, the roster is a list of players with keys: id,
    player and contract. Requires the team key already.
    Return
        team_dict with new roster key
    """

    team = team_dict['team']
    team_dict['roster'] = []
    roster = Contract.objects.filter(year=team.year, team=team.abbreviation)
    for r in roster:
        player = {
            'id': r.player.id,
            'player': r.player,
            'contract': r
        }
        team_dict['roster'].append(player)
    return team_dict


def collect_payroll(team_dict):
    """
    Takes a team_dict with a roster key and adds a payroll key. The payroll key contains a
    dictionary that has quick roster size info, gross and net payroll, payroll adjustments and
    remaining payroll. Requires the roster key already.
    return
        team_dict
    """
    fourty_five_man = len(team_dict['roster'])
    fourty_man = sum(1 for x in team_dict['roster'] if x['contract'].type != 'AA')
    gross_payroll = collect_salaries(team_dict)
    payroll_adjustments = collect_adjustment_totals(team_dict)
    net_payroll = [0, 0, 0, 0, 0]
    payroll_remaining = [0, 0, 0, 0, 0]
    for i in range(5):
        net_payroll[i] = gross_payroll[i] + payroll_adjustments[i]
        payroll_remaining[i] = 135000000 - net_payroll[i]
    team_dict['payroll'] = {
        '40_man': fourty_man,
        '45_man': fourty_five_man,
        'gross_payroll': gross_payroll,
        'payroll_adjustments': payroll_adjustments,
        'net_payroll': net_payroll,
        'payroll_remaining': payroll_remaining,
        'salary_cap': [135000000, 135000000, 135000000, 135000000, 135000000]
    }
    return team_dict


def collect_card_stats(team_dict):
    """
    Takes a team_dict with a roster key and adds a card_stats key, the card stats key includes a dictionary
    with 3 lists: hitters card stats, pitchers card stats and an uncarded players list.
    return
        team_dict
    """
    team_dict['card_stats'] = {
        'hitters': [],
        'pitchers': [],
        'uncarded': [],
    }
    for p in team_dict['roster']:
        hitter = HitterCardStats.objects.filter(player=p['id'], year=team_dict['team'].year)
        pitcher = PitcherCardStats.objects.filter(player=p['id'], year=team_dict['team'].year)
        if hitter.count():
            team_dict['card_stats']['hitters'].append(hitter[0])
        if pitcher.count():
            team_dict['card_stats']['pitchers'].append(pitcher[0])
        if (hitter.count() + pitcher.count()) == 0:
            team_dict['card_stats']['uncarded'].append(p['player'])
    return team_dict


def collect_salaries(team_dict):
    """
    Takes the team_dict, looks up all the salaries and sums them for the next 5 years.
    return
        list of 5 integers, the total of all the salaries
    """
    salaries = [0, 0, 0, 0, 0]
    for c in team_dict['roster']:
        for i in range(5):
            if (c['contract'].contract_season + i) <= c['contract'].length:
                salaries[i] += c['contract'].salary
    return salaries


def collect_adjustment_totals(team_dict):
    """
    Takes the team_dict, looks up all the adjustments and sums them for the next 5 years.
    return
        list of 5 integers, the total of all the payroll adjustments
    """
    franchise = team_dict['team'].franchise.id
    year = team_dict['team'].year
    adjustments = Payroll.objects.filter(
        Q(paying=franchise) | Q(receiving=franchise)
    )
    adjustments = adjustments.filter(year__gte=year).order_by('note', 'year')
    adjustments_list = [0, 0, 0, 0, 0]
    for a in adjustments:
        if a.receiving is not None:
            if a.receiving.id == franchise:
                adjustments_list[a.year - year] -= a.money
        if a.paying is not None:
            if a.paying.id == franchise:
                adjustments_list[a.year - year] += a.money
    return adjustments_list


def collect_adjustments(team_dict):
    """
    Takes the team_dict and adds the adjustment key, adjustment is a list of dicts with keys
    notes and money.
    return
        team_dict
    """
    team_dict['adjustment'] = []

    adjustments = Payroll.objects.filter(
        Q(paying=team_dict['team'].franchise) | Q(receiving=team_dict['team'].franchise)
    )
    adjustments = adjustments.filter(year__gte=team_dict['team'].year).order_by('note', 'year')
    for a in adjustments:
        money = a.money
        year = a.year - team_dict['team'].year
        if a.receiving is not None:
            if a.receiving == team_dict['team'].franchise:
                money = money * -1
        exists = False
        for d in team_dict['adjustment']:
            if a.note == d['note']:
                exists = True
        if exists:
            for d in team_dict['adjustment']:
                if a.note == d['note']:
                    d['money'][year] = money
        else:
            add_dict = {
                'note': a.note,
                'money': [0, 0, 0, 0, 0],
            }
            add_dict['money'][year] = money
            team_dict['adjustment'].append(add_dict.copy())
    return team_dict


def collect_contract_display(contract):
    """
    Takes a contract object and returns a dict for displaying that contract properly in the
    payroll view. Also verifies that the display list is at least 5 seasons long
    return
        contract dict with keys: contract, display, year_display
    """
    progression = ['AA', 'Y1', 'Y2', 'Y3', 'Arb4', 'Arb5', 'Arb6', 'FA', '', '', '']
    contract_dict = {
        'contract': contract,
        'display': contract.display_contract(),
        'year_display': []
    }
    contract_dict['year_display'].append(contract.salary)
    if contract.type in 'DFLUX':
        for i in range(min(contract.length - contract.contract_season, 4)):
            contract_dict['year_display'].append(contract.salary)
        if len(contract_dict['year_display']) < 5:
            contract_dict['year_display'].append('FA')
    else:
        t = contract.type
        if len(t) == 3:
            t = t[:2]
        season = progression.index(t)
        contract_dict['year_display'].extend(progression[season + 1:season + 5])
    while len(contract_dict['year_display']) < 5:
        contract_dict['year_display'].append('')
    return contract_dict


def collect_renewable(team_dict):
    """
    Takes team_dict and returns a list of dicts with the keys for players: id, player, contract.
    return
        arbitration (type list)
    """
    renewable = []
    renewable_list = ['AA', 'AAA', 'Y1', 'Y1*', 'Y2', 'Y2*', 'Y3', 'Y3*']
    for r in team_dict['roster']:
        if r['contract'].type in renewable_list:
            renewable.append(r)
    return renewable


def collect_guarenteed(team_dict):
    """
    Takes team_dict and returns a list of dicts with the keys for players: id, player, contract.
    return
        arbitration (type list)
    """
    guarenteed = []
    for r in team_dict['roster']:
        if r['contract'].type in 'DFLUX':
            guarenteed.append(r)
    return guarenteed


def collect_arbitration(team_dict):
    """
    Takes team_dict and returns a list of dicts with the keys for players: id, player, contract,
    minimum, median and maximum, the last 3 are related directly to the arbitration contract values.
    return
        arbitration (type list)
    """
    arbitration = []
    for r in team_dict['roster']:
        if 'Arb' in r['contract'].type:
            new_dict = {
                'contract': r['contract'],
                'id': r['id'],
                'player': r['player'],
            }
            new_arb = Arbitration.objects.filter(player=r['player'], year=r['contract'].year)[0]
            new_dict['minimum'] = new_arb.minimum_contract()
            new_dict['median'] = new_arb.median_contract()
            new_dict['maximum'] = new_arb.maximum_contract()
            arbitration.append(new_dict)
    return arbitration


def collect_draft_pick(team_dict):
    """
    Takes the team_dict and adds the draft_pick key, draft_pick is a list of dicts with keys
    pick and number.
    return
        team_dict
    """
    team_dict['draft_pick'] = []
    pick_list = DraftPick.objects.filter(owner=team_dict['team'].franchise.id,
                                         year=team_dict['team'].year)
    for p in pick_list:
        number = ((p.round - 1) * 16) + p.order
        dft_pick = {
            'pick': p,
            'number': number,
        }
        team_dict['draft_pick'].append(dft_pick)
    return team_dict

from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404

from league.models.players import Player, Contract, HitterCardStats, PitcherCardStats
from league.models.teams import Payroll, Team
from league.models.transactions import Arbitration, DraftPick


def collect_team_list_info(year):
    team_list_ = Team.objects.filter(year=year).order_by('location')
    team_list = []
    for t in team_list_:
        payroll = collect_payroll_elements(t.franchise.id, year)
        team_dict = {
            'payroll': payroll,
            'team': t,
        }
        team_list.append(team_dict)
    return team_list


def collect_payroll_adjustments(franchise, year):
    adjustments = Payroll.objects.filter(
        Q(paying=franchise) | Q(receiving=franchise)
    )
    adjustments = adjustments.filter(year__gte=year).order_by('note', 'year')
    return_data = []
    for a in adjustments:
        notes = a.note
        money = a.money
        if a.receiving is not None:
            if a.receiving.id == franchise:
                money = a.money * -1
        exists = False
        for r in return_data:
            if r['notes'] == notes:
                exists = True
        if exists:
            for r in return_data:
                if r['notes'] == notes:
                    r['adjustments'].append(money)
        else:
            if a.year == year:
                return_data.append({
                    'notes': notes,
                    'adjustments': [money, ],
                })
            elif a.year == year + 1:
                return_data.append({
                    'notes': notes,
                    'adjustments': [0, money, ],
                })
            elif a.year == year + 2:
                return_data.append({
                    'notes': notes,
                    'adjustments': [0, 0, money, ],
                })
    return return_data


def collect_total_payroll(team, year):
    contracts = get_list_or_404(Contract.objects.filter(year=year, team=team))
    total_payroll = [0, 0, 0, 0, 0]
    for c in contracts:
        guaranteed_years = c.length - c.contract_season + 1
        guaranteed_years = min(guaranteed_years, 5)
        for i in range(guaranteed_years):
            total_payroll[i] += c.salary
    return total_payroll, contracts


def collect_total_adjustments(adjustments):
    total_adjustments = [0, 0, 0, 0, 0]
    for a in adjustments:
        adjustment_years = len(a['adjustments'])
        for i in range(adjustment_years):
            total_adjustments[i] += a['adjustments'][i]
    return total_adjustments


def collect_team_header(team, year):
    team = get_object_or_404(Team, year=year, abbreviation=team)
    postseason = collect_postseason_data(team, year)
    header = {
        'team': team,
        'postseason': postseason,
    }
    return header


def collect_postseason_data(team, year):
    return None


def collect_off_season_contracts(team, year):
    contracts = Contract.objects.filter(year=year, team=team)
    # buyout list
    # early contract list
    early_contracts = ['AA', 'AAA', 'Y1', 'Y2', 'Y3', 'Y1*', 'Y2*', 'Y3*']
    early_contract_list = []
    # arbitration contract list
    arbitration_contracts = ['Arb4', 'Arb5', 'Arb6']
    arbitration_contract_list = []
    arbitration_info = []
    # guarneteed contract list
    guarenteed_contract_list = []
    players_signed, cards_signed = 0, 0
    for c in contracts:
        players_signed += 1
        if c.type != 'AA':
            cards_signed += 1
        if c.type in early_contracts:
            early_contract_list.append(c)
        elif c.type in arbitration_contracts:
            arbitration_contract_list.append(c)
            arb = get_object_or_404(Arbitration, year=year, player=c.player)
            arbitration_info.append(arb)
        else:
            guarenteed_contract_list.append(c)
    open_roster_slots = 45 - players_signed
    open_carded_slots = 40 - cards_signed
    contracts = {
        'early_contracts': early_contract_list,
        'arbitration_contracts': arbitration_contract_list,
        'arbitration_info': arbitration_info,
        'guarenteed_contracts': guarenteed_contract_list,
        'players_signed': players_signed,
        'cards_signed': cards_signed,
        'open_roster_slots': open_roster_slots,
        'open_carded_slots': open_carded_slots,
    }
    return contracts


def collect_payroll_elements(team, year):
    total_payroll, contracts = collect_total_payroll(team, year)
    adjustments = collect_payroll_adjustments(team, year)
    total_adjustments = collect_total_adjustments(adjustments)
    salary_cap = [135000000, 135000000, 135000000, 135000000, 135000000]
    net_payments = [0, 0, 0, 0, 0]
    net_remaining = [0, 0, 0, 0, 0]
    fourty_man = 0
    fourty_five_man = 0
    for c in contracts:
        fourty_five_man += 1
        if c.type != 'AA':
            fourty_man += 1
    for i in range(5):
        net_payments[i] = total_payroll[i] + total_adjustments[i]
        net_remaining[i] = salary_cap[i] - net_payments[i]
    payroll = {
        'contracts': contracts,
        'adjustments': adjustments,
        'total_payroll': total_payroll,
        'total_adjustments': total_adjustments,
        'salary_cap': salary_cap,
        'net_remaining': net_remaining,
        'net_payments': net_payments,
        '40_man': fourty_man,
        '45_man': fourty_five_man,
    }
    return payroll


def collect_draft_pick_list(team, year):
    draft_picks_ = DraftPick.objects.filter(year=year, owner=team).order_by('round', 'order')
    draft_picks = []
    for p in draft_picks_:
        number = ((p.round - 1) * 16) + p.order
        dft_pick = {
            'pick': p,
            'number': number,
        }
        draft_picks.append(dft_pick)
    return draft_picks


def collect_team_roster(team, year):
    collect_dict = {
        'roster': [],
        'hitters_card_stats': [],
        'pitchers_card_stats': [],
        'uncarded': [],
    }
    contracts = Contract.objects.filter(year=year, team=team)
    for c in contracts:
        plr_id = c.player_id
        collect_dict['roster'].append(plr_id)
        hitter_card_stats = HitterCardStats.objects.filter(year=year, player_id=plr_id)
        pitcher_card_stats = PitcherCardStats.objects.filter(year=year, player_id=plr_id)
        if len(hitter_card_stats) == 1:
            collect_dict['hitters_card_stats'].append(hitter_card_stats[0])
        if len(pitcher_card_stats) == 1:
            collect_dict['pitchers_card_stats'].append(pitcher_card_stats[0])
        if (len(hitter_card_stats) + len(pitcher_card_stats)) == 0:
            uncarded = Player.objects.filter(id = plr_id)[0]
            collect_dict['uncarded'].append(uncarded)

    return collect_dict

from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404

from league.models.players import Contract
from league.models.teams import Payroll, Team
from league.models.transactions import Arbitration


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
    }
    return payroll

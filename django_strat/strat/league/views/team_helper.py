from django.db.models import Q

from league.models.teams import Payroll


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


def collect_total_payroll(contracts):
    total_payroll = [0, 0, 0, 0, 0]
    for c in contracts:
        guaranteed_years = c.length - c.contract_season + 1
        guaranteed_years = min(guaranteed_years, 5)
        for i in range(guaranteed_years):
            total_payroll[i] += c.salary
    return total_payroll


def collect_total_adjustments(adjustments):
    total_adjustments = [0, 0, 0, 0, 0]
    for a in adjustments:
        adjustment_years = len(a['adjustments'])
        for i in range(adjustment_years):
            total_adjustments[i] += a['adjustments'][i]
    return total_adjustments


def collect_team_header(team, year):
    postseason = collect_postseason_data(team, year)
    header = {
        'postseason': postseason,
    }
    return header


def collect_postseason_data(team, year):
    return None

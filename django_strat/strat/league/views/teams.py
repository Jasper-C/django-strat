from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View

from league.models.players import Contract
from league.models.teams import Team
from league.views.team_helper import collect_payroll_adjustments,\
    collect_total_payroll, collect_total_adjustments


class TeamIndex(View):
    http_method_names = ['get']

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        team_list = Team.objects.filter(year=year).order_by('division', 'location')
        year_list = set(Team.objects.all().values_list("year", flat=True))
        next_year = year + 1
        last_year = year - 1

        context = {
            'team_list': team_list,
            'year_list': year_list,
            'year': year,
            'last_year': last_year,
            'next_year': next_year,
        }
        return render(request, 'league/team/index.html', context)


def team_detail(request, year, abbreviation):
    team = get_object_or_404(Team, year=year, abbreviation=abbreviation)
    roster = Contract.objects.filter(year=year, team=abbreviation)
    context = {
        'team': team,
        'roster': roster,
        'postseason': None,
        'hitting_stats': None,
        'pitching_stats': None,
    }
    return render(request, 'league/team/detail.html', context)


class TeamContracts(View):
    http_method_names = ['get']

    def get(self, request, year, abbreviation):
        team = get_object_or_404(Team, year=year, abbreviation=abbreviation)
        franchise = team.franchise.id
        contracts = Contract.objects.filter(year=year, team=franchise)
        adjustments = collect_payroll_adjustments(franchise, year)
        total_payroll = collect_total_payroll(contracts)
        total_adjustments = collect_total_adjustments(adjustments)
        salary_cap = [135000000, 135000000, 135000000, 135000000, 135000000]
        net_payments = [0, 0, 0, 0, 0]
        net_remaining = [0, 0, 0, 0, 0]
        for i in range(5):
            net_payments[i] = total_payroll[i] + total_adjustments[i]
            net_remaining[i] = salary_cap[i] - net_payments[i]
        context = {
            'team': team,
            'contracts': contracts,
            'adjustments': adjustments,
            'contract_list': ['Y1', 'Y2', 'Y3', 'Arb4', 'Arb5', 'Arb6', 'FA'],
            'total_payroll': total_payroll,
            'total_adjustments': total_adjustments,
            'salary_cap': salary_cap,
            'net_remaining': net_remaining,
            'net_payments': net_payments,
        }
        return render(request, 'league/team/contracts.html', context)

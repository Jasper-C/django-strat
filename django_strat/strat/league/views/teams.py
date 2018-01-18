from django.shortcuts import render
from django.utils import timezone
from django.views import View

from league.views.team_helper import *


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
    roster = Contract.objects.filter(year=year, team=abbreviation)
    header = collect_team_header(abbreviation, year)
    context = {
        'roster': roster,
        'header': header,
        'hitting_stats': None,
        'pitching_stats': None,
    }
    return render(request, 'league/team/detail.html', context)


class TeamContracts(View):
    http_method_names = ['get']

    def get(self, request, year, abbreviation):
        header = collect_team_header(abbreviation, year)
        franchise = header['team'].franchise.id
        payroll = collect_payroll_elements(franchise, year)
        context = {
            'header': header,
            'payroll': payroll,
            'contract_list': ['Y1', 'Y2', 'Y3', 'Arb4', 'Arb5', 'Arb6', 'FA'],
        }
        return render(request, 'league/team/contracts.html', context)


class TeamOffSeasonContracts(View):

    def get(self, request, year, abbreviation):
        header = collect_team_header(abbreviation, year)
        contracts = collect_off_season_contracts(abbreviation, year)
        payroll = collect_payroll_elements(abbreviation, year)
        context = {
            'contracts': contracts,
            'payroll': payroll,
            'header': header,
        }
        return render(request, 'league/team/off_season_contracts.html', context)

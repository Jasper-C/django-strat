from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from league.models.teams import Team, Payroll
from league.models.players import Player, Contract


class TeamIndex(View):

    def get(self, request, year):
        if year is None:
            year = timezone.now().year
        team_list = Team.objects.filter(year=year).order_by('division', 'location')
        year_list = set(Team.objects.all().values_list("year", flat=True))

        context = {
            'team_list': team_list,
            'year_list': year_list,
            'year': year,
        }
        return render(request, 'league/team/index.html', context)


def team_index(request, year):
    team_list = Team.objects.filter(year=year).order_by('division', 'location')
    if year is None:
        year = timezone.now().year
    context = {
        'team_list': team_list,
        'year': year,
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


def team_contracts(request, year, abbreviation):
    team = get_object_or_404(Team, year=year, abbreviation=abbreviation)
    contracts = Contract.objects.filter(year=year, team=abbreviation)
    payroll = Payroll.objects.filter(
        Q(paying=abbreviation) | Q(receiving=abbreviation)
    )
    payroll = payroll.filter(year__gte=year).order_by('year', 'note')
    context = {
        'team': team,
        'contracts': contracts,
        'payroll': payroll,
        'contract_list': ['Y1', 'Y2', 'Y3', 'Arb4', 'Arb5', 'Arb6', 'FA']
    }
    return render(request, 'league/team/contracts.html', context)

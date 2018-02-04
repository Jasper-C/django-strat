from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from league.forms.teams import RenewableArbitration, GuarenteedArbitration
from league.models.teams import Team
from league.views.team_helper import collect_teams, collect_team, collect_roster, \
    collect_payroll, collect_card_stats, collect_contract_display, collect_adjustments, \
    collect_renewable, collect_guarenteed, collect_arbitration


class TeamIndex(View):
    """
    Gets a list of the teams for a given year
    """
    http_method_names = ['get']

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        years = set(Team.objects.all().values_list("year", flat=True))
        next_year, last_year = None, None
        if year + 1 in years:
            next_year = year + 1
        if year - 1 in years:
            last_year = year - 1

        team_list = collect_teams(year)
        for t in team_list:
            t = collect_roster(t)
            t = collect_payroll(t)

        context = {
            'team_list': team_list,
            'year': year,
            'last_year': last_year,
            'next_year': next_year,
        }
        return render(request, 'league/team/index.html', context)


class TeamStats(View):
    http_method_names = ['get']

    def get(self, request, abbreviation, year=None):
        if year is None:
            year = timezone.now().year

        team = collect_team(year, abbreviation)
        context = {
            'team': team,
        }
        return render(request, 'league/team/stats.html', context)


# This view has been depricated
def team_detail(request, year, abbreviation):
    team = collect_team(year, abbreviation)
    team = collect_roster(team)
    context = {
        'team': team,
    }
    return render(request, 'league/team/detail.html', context)


class TeamContracts(View):
    http_method_names = ['get']

    def get(self, request, year, abbreviation):
        team = collect_team(year=year, abbreviation=abbreviation)
        team = collect_roster(team)
        team = collect_payroll(team)
        team = collect_adjustments(team)
        for r in team['roster']:
            r['contract'] = collect_contract_display(r['contract'])
        context = {
            'team': team,
            'contract_list': ['Y1', 'Y2', 'Y3', 'Arb4', 'Arb5', 'Arb6', 'FA'],
        }
        return render(request, 'league/team/contracts.html', context)


class TeamOffSeasonContracts(UserPassesTestMixin, View):

    def test_func(self):
        """
        Test If the current user owns the current team.

        Returns:
            bool
        """
        my_path = self.request.path.split('/')
        year = my_path[1]
        abbreviation = my_path[2]
        if self.request.method.lower() == 'get':
            return True
        try:
            Team.objects.get(owner=self.request.user, year=year, abbreviation=abbreviation)
        except Team.DoesNotExist:
            return False
        return True

    def get(self, request, year, abbreviation):
        header = collect_team_header(abbreviation, year)
        contracts = collect_off_season_contracts(abbreviation, year)
        payroll = collect_payroll_elements(abbreviation, year)
        is_owner = Team.objects.filter(owner=self.request.user, year=year, abbreviation=abbreviation).count()
        context = {
            'is_owner': is_owner,
            'contracts': contracts,
            'payroll': payroll,
            'header': header,
        }
        return render(request, 'league/team/off_season_contracts.html', context)

    def post(self):
        pass


class TeamDraftPickList(View):

    def get(self, request, year, abbreviation):
        draft_picks = collect_draft_pick_list(abbreviation, year)
        context = {
            'header': collect_team_header(abbreviation, year),
            'draft_picks': draft_picks,
        }
        return render(request, 'league/team/draft_picks.html', context)


class TeamRoster(View):
    """
    Gets a roster for a specific team, includes displays for player card stats
    """
    http_method_names = ['get']

    def get(self, request, year, abbreviation):
        team = collect_team(year, abbreviation)
        team = collect_roster(team)
        team = collect_card_stats(team)
        context = {
            'team': team,
        }
        return render(request, 'league/team/roster.html', context)


class TeamArbitration(View):

    def get(self, request, year, abbreviation):
        team = collect_team(year=year, abbreviation=abbreviation)
        team = collect_roster(team)
        team = collect_payroll(team)
        renewable = collect_renewable(team)
        guarenteed = collect_guarenteed(team)
        arbitration = collect_arbitration(team)
        renewable = RenewableArbitration(request.POST or None, renewable=renewable)
        guarenteed = GuarenteedArbitration(request.POST or None, guarenteed=guarenteed)
        context = {
            'team': team,
            'renewable': renewable,
            'guarenteed': guarenteed,
            'arbitration': arbitration,
        }
        return render(request, 'league/team/arbitration.html', context)

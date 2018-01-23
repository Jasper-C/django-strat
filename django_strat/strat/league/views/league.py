from django.shortcuts import render, get_list_or_404
from django.utils import timezone
from django.views import View

from league.models.teams import Team
from league.models.transactions import DraftPick, Trades


class LeagueDraftPicks(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        teams = get_list_or_404(Team.objects.filter(year=year))
        draft_picks = get_list_or_404(DraftPick.objects.filter(year=year)
                                      .order_by('round', 'order'))
        context = {
            'teams': teams,
            'draft_picks': draft_picks
        }
        return render(request, 'league/league/draft_picks.html', context)


class LeagueTradesIndex(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        trades = Trades.objects.all().order_by('date')
        print("Trades:")
        print(trades)
        context = {
            'trades': trades,
            'year': year,
        }
        return render(request, 'league/league/trades.html', context)

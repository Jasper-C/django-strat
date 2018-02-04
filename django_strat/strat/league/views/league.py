from django.shortcuts import render, get_list_or_404
from django.utils import timezone
from django.views import View

from league.models.teams import Team
from league.models.transactions import DraftPick, AvailableFreeAgent, AvailableDraftPick
from .league_helper import collect_trades, collect_trade


class LeagueDraft(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year
        context = {
            'year': year,
        }
        return render(request, 'league/league/draft.html', context)


class LeagueDraftPicks(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        teams = get_list_or_404(Team.objects.filter(year=year))
        picks = get_list_or_404(DraftPick.objects.filter(year=year)
                                      .order_by('round', 'order'))
        draft_picks = []
        for p in picks:
            number = ((p.round - 1) * 16) + p.order
            dft_pick = {
                'pick': p,
                'number': number,
            }
            draft_picks.append(dft_pick)
        context = {
            'teams': teams,
            'draft_picks': draft_picks
        }
        return render(request, 'league/league/draft_picks.html', context)


class LeagueDraftPlayers(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        draft_players = AvailableDraftPick.objects.filter(year=year)

        context = {
            'year': year,
            'draft_players': draft_players,
        }
        return render(request, 'league/league/draft_players.html', context)


class LeagueTradesIndex(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        trades = collect_trades(year)
        context = {
            'trades': trades,
            'year': year,
        }
        return render(request, 'league/league/trade_index.html', context)


class TradeDetail(View):

    def get(self, request, id):
        trade = collect_trade(id)
        context = {
            'trade': trade
        }
        return render(request, 'league/league/trade_detail.html', context)

class LeagueFreeAgentIndex(View):

    def get(self, request, year=None):
        if year is None:
            year = timezone.now().year

        free_agents = AvailableFreeAgent.objects.filter(year=year)
        context = {
            'free_agents': free_agents,
            'year': year,
        }
        return render(request, 'league/league/free_agents.html', context)

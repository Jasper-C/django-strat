from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic, View

from league.models.players import Player, HitterCardStats, PitcherCardStats
from .player_helper import collect_player_position, collect_team


class IndexView(generic.ListView):
    template_name = 'league/player/index.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        return Player.objects.all()


class PlayerDetail(View):

    def get(self, request, player_id):
        player = get_object_or_404(Player, pk=player_id)
        hitting_card_stats = HitterCardStats.objects.filter(player=player_id).order_by('year')
        pitching_card_stats = PitcherCardStats.objects.filter(player=player_id).order_by('year')
        positions = collect_player_position(player)
        year = timezone.now().year
        teams = collect_team(player, year)
        context = {
            'player': player,
            'bats': player.batting_hand(),
            'throws': player.throwing_hand(),
            'positions': positions,
            'teams': teams,
            'hitting_card_stats': hitting_card_stats,
            'pitching_card_stats': pitching_card_stats,
        }
        return render(request, 'league/player/detail.html', context)

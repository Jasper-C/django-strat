from django.views import generic
from django.shortcuts import render, get_object_or_404

from league.models.players import Player


class IndexView(generic.ListView):
    template_name = 'league/player/index.html'
    context_object_name = 'player_list'
    
    def get_queryset(self):
        return Player.objects.all()
    

def detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {
        'player': player,
        'bats': player.batting_hand(),
        'throws': player.throwing_hand(),
    }
    return render(request, 'league/player/detail.html', context)

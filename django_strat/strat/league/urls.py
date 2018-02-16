from django.urls import path

from .views import players, teams, league

app_name = 'league'
urlpatterns = [
    path('players/', players.IndexView.as_view(), name='player_index'),
    path('players/<str:player_id>/', players.PlayerDetail.as_view(), name='player_detail'),
    # path('players/<str:player_id>/contract', views.contract, name='player_contract'),
    path('teams/', teams.TeamIndex.as_view(), name='team_index'),
    path('teams/<int:year>', teams.TeamIndex.as_view(), name='team_index'),
    path('teams/<int:year>/<str:abbreviation>/', teams.TeamRoster.as_view(), name='team_roster'),
    path('teams/<int:year>/<str:abbreviation>/stats/', teams.TeamRoster.as_view(), name='team_stats'),
    path('teams/<int:year>/<str:abbreviation>/roster/', teams.TeamRoster.as_view(), name='team_roster'),
    path('teams/<int:year>/<str:abbreviation>/contracts/', teams.TeamContracts.as_view(), name='team_contracts'),
    path('teams/<int:year>/<str:abbreviation>/arbitration/', teams.TeamArbitration.as_view(),
         name='team_arbitration'),
    path('teams/<int:year>/<str:abbreviation>/draft_picks/',
         teams.TeamDraftPick.as_view(), name='team_draft_picks'),
    path('draft', league.LeagueDraft.as_view(), name='draft'),
    path('draft/<int:year>/picks_index', league.LeagueDraftPicks.as_view(), name='draft_picks_index'),
    path('draft/<int:year>/players_index', league.LeagueDraftPlayers.as_view(), name='draft_players_index'),
    path('trades', league.LeagueTradesIndex.as_view(), name='trades_index'),
    path('trades/<int:id>', league.TradeDetail.as_view(), name='trade_detail'),
    path('free_agents', league.LeagueFreeAgentIndex.as_view(), name='free_agent_index'),
    ]

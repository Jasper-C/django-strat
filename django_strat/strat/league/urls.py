from django.urls import path

from .views import players, teams, league

app_name = 'league'
urlpatterns = [
    path('players/', players.IndexView.as_view(), name='player_index'),
    path('players/<str:player_id>/', players.detail, name='player_detail'),
    # path('players/<str:player_id>/contract', views.contract, name='player_contract'),
    path('teams/', teams.TeamIndex.as_view(), name='team_index'),
    path('teams/<int:year>', teams.TeamIndex.as_view(), name='team_index'),
    path('teams/<int:year>/<str:abbreviation>/', teams.team_detail, name='team_detail'),
    path('teams/<int:year>/<str:abbreviation>/stats/', teams.team_detail, name='team_stats'),
    path('teams/<int:year>/<str:abbreviation>/roster/', teams.team_detail, name='team_roster'),
    path('teams/<int:year>/<str:abbreviation>/contracts/', teams.TeamContracts.as_view(), name='team_contracts'),
    path('teams/<int:year>/<str:abbreviation>/off_season/', teams.TeamOffSeasonContracts.as_view(),
         name='team_off_season'),
    path('teams/<int:year>/<str:abbreviation>/draft_picks/',
         teams.TeamDraftPickList.as_view(), name='team_draft_picks'),
    path('draft', league.LeagueDraftPicks.as_view(), name='draft_picks'),
    path('trades', league.LeagueTradesIndex.as_view(), name='trades_index'),
    ]

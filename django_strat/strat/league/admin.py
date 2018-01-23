from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Player, Franchise, Team, \
    Ballpark, Payroll, Contract, Arbitration, \
    DraftPick, Trades, TradePlayer, TradePick, TradeMoney


@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    fieldsets = [
        ('Player ID',       {'fields': ['id']}),
        ('Player Info',     {'fields': [
            'first_name', 'last_name', 'player_type',
            'birth_year', 'bats', 'throws', 'active',
        ]}),
        ('Website Lookups', {'fields': [
            'bbref_id', 'mlb_id', 'bp_id',
            'cbs_id', 'espn_id', 'fg_id'
        ]}),
    ]


@admin.register(Contract)
class ContractAdmin(ImportExportModelAdmin):
    fields = [
        'player',
        'type',
        'year',
        'contract_season',
        'length',
        'salary',
        'team'
    ]


@admin.register(Franchise)
class FranchiseAdmin(ImportExportModelAdmin):
    fields = [
        'id',
        'location',
        'nickname',
        'owner'
    ]


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    fields = [
        'id',
        'year',
        'abbreviation',
        'franchise',
        'location',
        'nickname',
        'owner',
        'division',
        'ballpark'
    ]


@admin.register(Ballpark)
class BallparkAdmin(ImportExportModelAdmin):
    fields = [
        'id',
        'name',
        'location',
        'year',
        'singles_left',
        'singles_right',
        'homeruns_left',
        'homeruns_right'
    ]


@admin.register(Payroll)
class PayrollAdmin(ImportExportModelAdmin):
    fields = [
        'receiving',
        'paying',
        'year',
        'money',
        'note'
    ]


@admin.register(Arbitration)
class ArbitrationAdmin(ImportExportModelAdmin):
    fields = [
        'player',
        'year',
        'type',
        'war_sub_0',
        'war_sub_1',
        'war_sub_2',
        'war_sub_3',
    ]


@admin.register(DraftPick)
class DraftPickAdmin(ImportExportModelAdmin):
    fields = [
        'year',
        'round',
        'order',
        'original_team',
        'owner',
        'player',
        'time',
        'passed',
    ]


@admin.register(Trades)
class TradesAdmin(ImportExportModelAdmin):
    fields = [
        'date',
        'year',
        'teams',
        'notes',
        'story',
    ]


@admin.register(TradePlayer)
class TradePlayerAdmin(ImportExportModelAdmin):
    fields = [
        'trade',
        'team_receiving',
        'team_giving',
        'player',
    ]


@admin.register(TradePick)
class TradePickAdmin(ImportExportModelAdmin):
    fields = [
        'trade',
        'team_receiving',
        'team_giving',
        'draft_pick',
    ]


@admin.register(TradeMoney)
class TradeMoneyAdmin(ImportExportModelAdmin):
    fields = [
        'trade',
        'team_receiving',
        'team_giving',
        'money',
        'year',
        'payroll_note',
    ]

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import Player, Franchise, Team, \
    Ballpark, Payroll, Contract


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
        'salary'
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

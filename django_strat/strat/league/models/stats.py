from django.db import models

from league.models.players import Player


class PlayerMLBStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    year = models.IntegerField()
    age = models.IntegerField()
    team = models.CharField(max_length=3)
    lg = models.CharField(max_length=3, verbose_name="MLB League")
    season_segment = models.IntegerField(default=0)
    war = models.DecimalField(max_digits=5, decimal_places=2)
    awards = models.CharField(max_length=50)


class HitterMLBStats(PlayerMLBStats):
    games = models.IntegerField()
    plate_appearances = models.IntegerField()
    at_bats = models.IntegerField()
    runs = models.IntegerField()
    hits = models.IntegerField()
    doubles = models.IntegerField()
    triples = models.IntegerField()
    home_runs = models.IntegerField()
    runs_batted_in = models.IntegerField()
    stolen_bases = models.IntegerField()
    caught_stealing = models.IntegerField()
    walks = models.IntegerField()
    strikeouts = models.IntegerField()
    grounded_into_double_play = models.IntegerField()
    hit_by_pitch = models.IntegerField()
    sacrifice_hit = models.IntegerField()
    sacrifice_fly = models.IntegerField()
    intentional_walks = models.IntegerField()
    positions = models.CharField(max_length=30)


class PitcherMLBStats(PlayerMLBStats):
    wins = models.IntegerField()
    losses = models.IntegerField()
    games = models.IntegerField()
    game_started = models.IntegerField()
    games_finished = models.IntegerField()
    complete_games = models.IntegerField()
    shutouts = models.IntegerField()
    saves = models.IntegerField()
    outs_recorded = models.IntegerField()
    hits_allowed = models.IntegerField()
    runs_allowed = models.IntegerField()
    earned_runs = models.IntegerField()
    home_runs_allowed = models.IntegerField()
    walks = models.IntegerField()
    intentional_walks = models.IntegerField()
    strikeouts = models.IntegerField()
    hit_by_pitch = models.IntegerField()
    balk = models.IntegerField()
    wild_pitch = models.IntegerField()
    batters_faced = models.IntegerField()


class PlayerMLBSplitStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    year = models.IntegerField()
    side = models.CharField(max_length=1)
    plate_appearances = models.IntegerField(null=True, blank=True)
    at_bats = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    doubles = models.IntegerField(null=True, blank=True)
    triples = models.IntegerField(null=True, blank=True)
    home_runs = models.IntegerField(null=True, blank=True)
    walks = models.IntegerField(null=True, blank=True)
    strikeouts = models.IntegerField(null=True, blank=True)
    grounded_into_double_play = models.IntegerField(null=True, blank=True)
    hit_by_pitch = models.IntegerField(null=True, blank=True)
    intentional_walks = models.IntegerField(null=True, blank=True)

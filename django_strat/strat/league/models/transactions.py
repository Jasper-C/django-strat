from decimal import *

from django.contrib.auth import get_user_model as User
from django.db import models
from django.utils import timezone

from .players import Player, Contract
from .teams import Franchise


class Arbitration(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    year = models.IntegerField(default=1)
    type = models.CharField(max_length=6)
    war_sub_0 = models.DecimalField(max_digits=3, decimal_places=1)
    war_sub_1 = models.DecimalField(max_digits=3, decimal_places=1)
    war_sub_2 = models.DecimalField(max_digits=3, decimal_places=1)
    war_sub_3 = models.DecimalField(max_digits=3, decimal_places=1)

    def minimum_contract_value(self):
        min_contract = 0
        if self.type == 'Arb4':
            min_contract = 850000
        elif self.type == 'Arb5':
            min_contract = 1000000
            previous_contract = Contract.objects.filter(year=int(self.year)-1, player=self.player)
            salary = previous_contract[0].salary
            if salary > min_contract:
                min_contract = salary
        elif self.type == 'Arb6':
            min_contract = 1250000
            previous_contract = Contract.objects.filter(year=int(self.year)-1, player=self.player)
            salary = previous_contract[0].salary
            if salary > min_contract:
                min_contract = salary
        return min_contract
    # TODO: Find previous contract and insert into minimum contract

    class Meta:
        ordering = ['-year', 'player']

    def __str__(self):
        return "{}, {}".format(self.player.last_name, self.player.first_name)

    def war_value(self):
        war = Decimal(0)
        war += max(Decimal(self.war_sub_0), Decimal('0.5')) * 10
        war += max(Decimal(self.war_sub_1), Decimal('0.5')) * 6
        war += max(Decimal(self.war_sub_2), Decimal('0.5')) * 4
        war += max(Decimal(self.war_sub_3), Decimal('0.5')) * 3
        war = war / Decimal('23')
        war = war * Decimal('1250000')
        return war

    def minimum_contract(self):
        if self.type == 'Arb4':
            min_value = self.war_value() * Decimal('0.638')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value
        elif self.type == 'Arb5':
            min_value = self.war_value() * Decimal('0.788')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value
        elif self.type == 'Arb6':
            min_value = self.war_value() * Decimal('1.038')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value

    def median_contract(self):
        if self.type == 'Arb4':
            min_value = self.war_value() * Decimal('0.850')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value
        elif self.type == 'Arb5':
            min_value = self.war_value() * Decimal('1.000')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value
        elif self.type == 'Arb6':
            min_value = self.war_value() * Decimal('1.250')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value

    def maximum_contract(self):
        if self.type == 'Arb4':
            min_value = self.war_value() * Decimal('1.062')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value
        elif self.type == 'Arb5':
            min_value = self.war_value() * Decimal('1.212')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value
        elif self.type == 'Arb6':
            min_value = self.war_value() * Decimal('1.462')
            min_value = int(round(float(min_value) / 25000.0) * 25000.0)
            if min_value < self.minimum_contract_value():
                return self.minimum_contract_value()
            else:
                return min_value


class DraftPick(models.Model):
    year = models.IntegerField()
    round = models.IntegerField()
    order = models.IntegerField(null=True, blank=True, verbose_name="Order in Round")
    original_team = models.ForeignKey(Franchise,
                                      related_name='original',
                                      on_delete=models.PROTECT)
    owner = models.ForeignKey(Franchise,
                              verbose_name='Owner of Pick',
                              related_name='pick_owner',
                              on_delete=models.PROTECT)
    player = models.ForeignKey(Player,
                               null=True, blank=True,
                               verbose_name="Player Selected",
                               on_delete=models.PROTECT)
    time = models.DateTimeField(null=True, blank=True,
                                verbose_name="Date/Time Selected")
    passed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year', 'order', 'round']

    def toOrdinalNum(self):
        return str(self.round) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= int(self.round) % 100 < 20 else int(self.round) % 10, "th")

    def __str__(self):
        return "{}'s {} round pick-{}".format(self.original_team.location, self.toOrdinalNum(), self.year)


class Trades(models.Model):
    date = models.DateTimeField()
    year = models.IntegerField(verbose_name="League Season")
    teams = models.ManyToManyField(Franchise)
    notes = models.TextField(null=True, blank=True)
    story = models.TextField(null=True, blank=True)


class TradePart(models.Model):
    trade = models.ForeignKey(Trades, on_delete=models.PROTECT)
    team_receiving = models.ForeignKey(Franchise,
                                       related_name='receiving_in_trade',
                                       on_delete=models.PROTECT)
    team_giving = models.ForeignKey(Franchise,
                                    related_name='giving_in_trade',
                                    on_delete=models.PROTECT)


class TradePlayer(TradePart):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)


class TradePick(TradePart):
    draft_pick = models.ForeignKey(DraftPick,
                                   on_delete=models.PROTECT)


class TradeMoney(TradePart):
    money = models.IntegerField()
    year = models.IntegerField(verbose_name='Effective In Year')
    payroll_note = models.TextField()


class AvailableDraftPick(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    year = models.IntegerField()
    contract = models.CharField(max_length=4)
    salary = models.IntegerField()

    class Meta:
        ordering = ['-year', 'player']

    def __str__(self):
        return '{}, {}-Draft Pick'.format(self.player.last_name,
                                          self.player.first_name)


class AvailableFreeAgent(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    year = models.IntegerField()
    bid_time_stamp = models.DateTimeField(null=True, blank=True)
    bid_team = models.ForeignKey(Franchise, on_delete=models.PROTECT, null=True, blank=True)
    bid_length = models.IntegerField(null=True, blank=True)
    bid_salary = models.IntegerField(null=True, blank=True)
    auction_starts = models.DateTimeField(null=True, blank=True)
    auction_ends = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-year', 'player']

    def __str__(self):
        return '{}, {}-Free Agent'.format(self.player.last_name, self.player.first_name)

    def bid_value(self):
        if self.bid_time_stamp is None:
            return None
        else:
            multiplier = [0, Decimal('1.00'), Decimal('1.55'), Decimal('1.90'), Decimal('2.20'),
                          Decimal('2.45'), Decimal('2.65'), Decimal('2.80')]
            value = multiplier[int(str(self.bid_length))] * self.bid_salary
            return int(value)

    def auction_in_progress(self):
        if timezone.now() < self.auction_starts:
            return False
        elif timezone.now() > self.auction_ends:
            return False
        else:
            return True


class FreeAgentBid(models.Model):
    free_agent = models.ForeignKey(AvailableFreeAgent, on_delete=models.CASCADE)
    bid_time_stamp = models.DateTimeField()
    bid_team = models.ForeignKey(Franchise, on_delete=models.PROTECT)
    bid_length = models.IntegerField()
    bid_salary = models.IntegerField()
    user = models.ForeignKey(User(), on_delete=models.PROTECT)

    class Meta:
        ordering = ['free_agent', '-bid_time_stamp']

    def __str__(self):
        return '{}, {}-{}-Free Agent Bid'.format(self.free_agent.last_name,
                                                 self.free_agent.first_name,
                                                 self.bid_time_stamp)

    def is_high_bid(self):
        if self.bid_time_stamp == self.free_agent.bid_time_stamp:
            return True
        else:
            return False

from django.db import models


class Player(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    player_type = models.CharField(max_length=2)
    active = models.BooleanField(default=True)
    bats = models.CharField(max_length=1)
    throws = models.CharField(max_length=1)
    birth_year = models.IntegerField()
    bbref_id = models.CharField(max_length=20)
    mlb_id = models.CharField(max_length=10)
    bp_id = models.CharField(max_length=10)
    cbs_id = models.CharField(max_length=10)
    espn_id = models.CharField(max_length=10)
    fg_id = models.CharField(max_length=10)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    def batting_hand(self):
        if self.bats.lower() == 'l':
            return 'Left'
        elif self.bats.lower() == 'r':
            return 'Right'
        elif self.bats.lower() == 's' or self.bats.lower() == 'b':
            return 'Both'
        else:
            return 'Unknown'

    def throwing_hand(self):
        if self.throws.lower() == 'l':
            return 'Left'
        elif self.throws.lower() == 'r':
            return 'Right'
        elif self.throws.lower() == 's' or self.bats.lower() == 'b':
            return 'Both'
        else:
            return 'Unknown'


class Contract(models.Model):
    player = models.ForeignKey(Player, db_column='player_id', on_delete=models.CASCADE)
    type = models.CharField(max_length=8)
    year = models.IntegerField(default=1)
    contract_season = models.IntegerField(default=1)
    length = models.IntegerField()
    salary = models.IntegerField()
    team = models.ForeignKey('league.Franchise', db_column='team', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-year', 'player']

    def __str__(self):
        return '{}, {} - {} Contract'.format(self.player.last_name, self.player.first_name, self.year)

    contract_advance = {
        0: 'AA',
        1: 'Y1',
        2: 'Y2',
        3: 'Y3',
        4: 'Arb4',
        5: 'Arb5',
        6: 'Arb6',
        7: 'FA',
        8: '',
    }

    contract_year = {
        'AA': 0,
        'AAA': 0,
        'Y1': 1,
        'Y1*': 1,
        'Y2': 2,
        'Y2*': 2,
        'Y3': 3,
        'Y3*': 3,
        'Arb4': 4,
        'Arb5': 5,
        'Arb6': 6,
    }

    def display_contract(self):
        contract = ''
        if self.type in ['AA', 'AAA', 'Y1', 'Y2', 'Y3', 'Y1*', 'Y2*', 'Y3*']:
            contract += self.type
        else:
            if self.type in ['Arb4', 'Arb5', 'Arb6']:
                contract += self.type + ', '
            else:
                contract += '{}-{} {}, '.format(self.contract_season, self.length, self.type)
            if int(self.salary) >= 1000000:
                contract += '${:.2f}M'.format(int(self.salary)/1000000)
            else:
                contract += '${:.0f}k'.format(int(self.salary)/1000)
        return contract

    def plus(self, yrs):
        if self.type in self.contract_year:
            return self.contract_advance[min(self.contract_year[self.type] + yrs, 8)]
        else:
            if self.contract_season + yrs <= self.length:
                return '${:,}'.format(self.salary)
            elif self.contract_season + yrs - 1 == self.length:
                return 'FA'
            else:
                return ''

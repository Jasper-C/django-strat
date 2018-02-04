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
    bbref_id = models.CharField(max_length=20, null=True, blank=True)
    mlb_id = models.CharField(max_length=10, null=True, blank=True)
    bp_id = models.CharField(max_length=10, null=True, blank=True)
    cbs_id = models.CharField(max_length=10, null=True, blank=True)
    espn_id = models.CharField(max_length=10, null=True, blank=True)
    fg_id = models.CharField(max_length=10, null=True, blank=True)

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
        return '{}, {} - {}'.format(self.player.last_name, self.player.first_name, self.year)

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


class PlayerCardStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.IntegerField()
    team = models.CharField(max_length=3, verbose_name='MLB Team')
    so_left = models.IntegerField()
    bb_left = models.IntegerField()
    hits_left = models.IntegerField()
    onbase_left = models.IntegerField()
    totalbase_left = models.IntegerField()
    homeruns_left = models.IntegerField()
    gba_left = models.IntegerField()
    triangles_left = models.IntegerField()
    diamonds_left = models.IntegerField()
    so_right = models.IntegerField()
    bb_right = models.IntegerField()
    hits_right = models.IntegerField()
    onbase_right = models.IntegerField()
    totalbase_right = models.IntegerField()
    homeruns_right = models.IntegerField()
    gba_right = models.IntegerField()
    triangles_right = models.IntegerField()
    diamonds_right = models.IntegerField()
    stealing = models.CharField(max_length=40)
    running = models.IntegerField()
    bunt_rating = models.CharField(max_length=1)
    hit_run_rating = models.CharField(max_length=1)

    class Meta:
        ordering = ['-year', 'player']

    def h_l(self):
        return '{:3.0f}'.format(self.hits_left / 20)

    def ob_l(self):
        return '{:3.0f}'.format(self.onbase_left / 20)

    def tb_l(self):
        return '{:3.0f}'.format(self.totalbase_left / 20)

    def hr_l(self):
        return '{:4.1f}'.format(self.homeruns_left / 20)

    def gba_l(self):
        return '{:2.0f}'.format(self.homeruns_left / 20)

    def h_r(self):
        return '{:3.0f}'.format(self.hits_right / 20)

    def ob_r(self):
        return '{:3.0f}'.format(self.onbase_right / 20)

    def tb_r(self):
        return '{:3.0f}'.format(self.totalbase_right / 20)

    def hr_r(self):
        return '{:4.1f}'.format(self.homeruns_right / 20)

    def gba_r(self):
        return '{:2.0f}'.format(self.homeruns_right / 20)


class HitterCardStats(PlayerCardStats):
    clutch_left = models.IntegerField()
    power_left = models.BooleanField()
    clutch_right = models.IntegerField()
    power_right = models.BooleanField()
    def_catcher_range = models.IntegerField(null=True, blank=True)
    def_catcher_error = models.IntegerField(null=True, blank=True)
    def_firstbase_range = models.IntegerField(null=True, blank=True)
    def_firstbase_error = models.IntegerField(null=True, blank=True)
    def_secondbase_range = models.IntegerField(null=True, blank=True)
    def_secondbase_error = models.IntegerField(null=True, blank=True)
    def_thirdbase_range = models.IntegerField(null=True, blank=True)
    def_thirdbase_error = models.IntegerField(null=True, blank=True)
    def_shortstop_range = models.IntegerField(null=True, blank=True)
    def_shortstop_error = models.IntegerField(null=True, blank=True)
    def_leftfield_range = models.IntegerField(null=True, blank=True)
    def_leftfield_error = models.IntegerField(null=True, blank=True)
    def_centerfield_range = models.IntegerField(null=True, blank=True)
    def_centerfield_error = models.IntegerField(null=True, blank=True)
    def_rightfield_range = models.IntegerField(null=True, blank=True)
    def_rightfield_error = models.IntegerField(null=True, blank=True)
    def_outfield_arm = models.IntegerField(null=True, blank=True)
    def_catcher_arm = models.IntegerField(null=True, blank=True)
    def_catcher_passedball = models.IntegerField(null=True, blank=True)
    def_catcher_t_rating = models.IntegerField(null=True, blank=True)
    defensive_string = models.CharField(null=True, blank=True, max_length=100)

    def bp_l(self):
        bp = ''
        if not self.power_left:
            bp += 'w'
        else:
            bp += '{}'.format(self.diamonds_left)
        if self.triangles_left == 0:
            bp += '\u25bc'
        return bp

    def cl_l(self):
        return '{:+d}'.format(self.clutch_left)

    def bp_r(self):
        bp = ''
        if not self.power_right:
            bp += 'w'
        else:
            bp += '{}'.format(self.diamonds_right)
        if self.triangles_right == 0:
            bp += '\u25bc'
        return bp

    def cl_r(self):
        return '{:+d}'.format(self.clutch_right)


class PitcherCardStats(PlayerCardStats):
    starter_endurance = models.IntegerField(null=True, blank=True)
    relief_endurance = models.IntegerField(null=True, blank=True)
    closer_rating = models.IntegerField(null=True, blank=True)
    hold = models.IntegerField()
    wild_pitch = models.IntegerField()
    balk = models.IntegerField()
    def_range = models.IntegerField()
    def_error = models.IntegerField()
    pitcher_hitting_card = models.IntegerField()
    power = models.BooleanField()

    def bp_l(self):
        if self.triangles_left == 0:
            return '{}'.format(self.diamonds_left) + '\u25bc'
        else:
            return '{}'.format(self.diamonds_left)

    def bp_r(self):
        if self.triangles_right == 0:
            return '{}'.format(self.diamonds_right) + '\u25bc'
        else:
            return '{}'.format(self.diamonds_right)

    def hold_rating(self):
        return '{:+d}'.format(self.hold)

    def phc(self):
        power = 'W'
        if self.power:
            power = 'N'
        return '{}{}{}-{}'.format(self.pitcher_hitting_card, power, self.player.bats.upper(), self.bunt_rating)

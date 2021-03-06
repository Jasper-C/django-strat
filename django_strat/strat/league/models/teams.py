from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Ballpark(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=75)
    location = models.CharField(max_length = 50)
    year = models.IntegerField()
    singles_left = models.IntegerField()
    singles_right = models.IntegerField()
    homeruns_left = models.IntegerField()
    homeruns_right = models.IntegerField()

    class Meta:
        ordering = ['-year', 'location']

    def __str__(self):
        return '{} {} Ballpark'.format(self.year, self.location)


class Franchise(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    owner = models.ForeignKey(User, db_column='current_owner', null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)

    class Meta:
        ordering = ['location']

    def __str__(self):
        return '{} {} Franchise'.format(self.location, self.nickname)


class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    year = models.IntegerField()
    abbreviation = models.CharField(max_length=5)
    franchise = models.ForeignKey(Franchise, db_column='franchise', on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    owner = models.ForeignKey(User, db_column='owner', null=True, on_delete=models.SET_NULL)
    # Setting up division choices
    ALW = 'ALW'
    ALE = 'ALE'
    NLW = 'NLW'
    NLE = 'NLE'
    division_choices = (
        (ALW, 'AL West'),
        (ALE, 'AL East'),
        (NLW, 'NL West'),
        (NLE, 'NL East'),
    )
    division = models.CharField(max_length=12, choices=division_choices)
    ballpark = models.ForeignKey(Ballpark, db_column='ballpark', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-year', 'location']

    def __str__(self):
        return '{} {} {}'.format(self.year, self.location, self.nickname)


class Payroll(models.Model):
    receiving = models.ForeignKey(Franchise,
                                  db_column='receiving',
                                  null=True, blank=True,
                                  related_name='receiving',
                                  on_delete=models.SET_NULL)
    paying = models.ForeignKey(Franchise,
                               db_column='paying',
                               null=True, blank=True,
                               related_name='paying',
                               on_delete=models.SET_NULL)
    year = models.IntegerField()
    money = models.IntegerField()
    note = models.TextField()

    class Meta:
        ordering = ['year', 'note']

    def __str__(self):
        return '<Payroll Adjustment: {} {}>'.format(self.year, self.note)


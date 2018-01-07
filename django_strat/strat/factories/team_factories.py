import factory
from factory.django import DjangoModelFactory
from league.models import Team, Ballpark, Franchise


class BallparkFactory(DjangoModelFactory):

    class Meta:

        model = Ballpark
    id = factory.Sequence(lambda n: "%003d" % n)
    name = factory.Sequence(lambda n: "Default Ballpark Name %003d" % n)
    location = factory.Sequence(lambda n: "Default Ballpark Location %003d" % n)
    year = 2017
    singles_left = 5
    singles_right = 5
    homeruns_left = 5
    homeruns_right = 5


class FranchiseFactory(DjangoModelFactory):

    class Meta:

        model = Franchise
    id = factory.Sequence(lambda n: "%003d" % n)
    nickname = factory.Sequence(lambda n: "Default Franchise Name %003d" % n)
    location = factory.Sequence(lambda n: "Default Franchise Location %003d" % n)


class TeamFactory(DjangoModelFactory):

    class Meta:

        model = Team
    id = factory.Sequence(lambda n: "%003d" % n)
    year = 2017
    abbreviation = factory.Sequence(lambda n: "T%0004d" % n)
    nickname = factory.Sequence(lambda n: "Default Team Name %003d" % n)
    location = factory.Sequence(lambda n: "Default Team Location %003d" % n)
    franchise = factory.SubFactory(FranchiseFactory, nickname=factory.Sequence(lambda n: "Team Franchise %003d" % n))
    division = 'ALW'
    ballpark = factory.SubFactory(BallparkFactory)

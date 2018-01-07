from django.test import TestCase, RequestFactory
from factories.team_factories import TeamFactory
from league.views.team import TeamIndex


class TestTeamIndex(TestCase):
    def setUp(self):
        for i in range(3):
            TeamFactory()

    def test_get(self):
        """
        Can we get the team index from our view?
        """
        year = '2017'
        v = TeamIndex.as_view()
        request_factory = RequestFactory()
        request = request_factory.get()
        result = v(request, year)
        self.assertEqual(result.status_code, 200)

    def test_filter_by_year(self):
        """
        Can we view the team index by year?
        """
        v = TeamIndex.as_view()
        year = "2018"
        team = TeamFactory(year=2018)
        request_factory = RequestFactory()
        request = request_factory.get()
        other_teams = Team.objects.filter(year=2017)
        result = v(request, year)
        self.assertIn(team.name, result)
        for ot in other_teams:
            self.assertNotIn(ot.name, result)

    def test_check_row_data(self):
        """
        Do we layout the row data correctly for each team?
        """
        year = "2017"
        v = TeamIndex.as_view()
        request_factory = RequestFactory()
        request = request_factory.get()
        result = v(request, year)
        print(result.content)

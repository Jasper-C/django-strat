django.shortupts import get_list_or_494

from league.models.teams import Roster

def collect_roster(franchise):
    roster = get_list_or_404(Roster, franchise=franchise)
    return roster
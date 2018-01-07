from django.db.models import Q

from league.models.teams import Payroll


def collect_payroll_adjustments(franchise, year):
    adjustments = Payroll.objects.filter(
        Q(paying=franchise) | Q(receiving=franchise)
    )
    adjustments = adjustments.filter(year__gte=year).order_by('note', 'year')
    return_data = []
    for a in adjustments:
        notes = a.note
        money = a.money
        if a.receiving is not None:
            if a.receiving.id == franchise:
                money = a.money * -1
        exists = False
        for r in return_data:
            if r['notes'] == notes:
                exists = True
        if exists:
            for r in return_data:
                if r['notes'] == notes:
                    r['adjustments'].append(money)
        else:
            return_data.append({
                'notes': notes,
                'adjustments': [money, ],
            })
    return return_data

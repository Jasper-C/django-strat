from django import forms

renewable_choices = (
    ('keep', 'Keep'),
    ('ltc', 'Long Term Contract'),
    ('rel', 'Release'),
)

guarenteed_choices = (
    ('keep', 'Keep'),
    ('rel', 'Release'),
)


class RenewableArbitration(forms.Form):

    def __init__(self, *args, **kwargs):
        renewable = kwargs.pop('renewable')
        super(RenewableArbitration, self).__init__(*args, **kwargs)

        for i, player in enumerate(renewable):
            self.fields['{}'.format(player['id'])] = \
                forms.MultipleChoiceField(choices=renewable_choices,
                                          widget=forms.RadioSelect,
                                          label='{}, {}'.format(player['player'].last_name,
                                                                player['player'].first_name))


class GuarenteedArbitration(forms.Form):

    def __init__(self, *args, **kwargs):
        guarenteed = kwargs.pop('guarenteed')
        super(GuarenteedArbitration, self).__init__(*args, **kwargs)

        for i, player in enumerate(guarenteed):
            self.fields['{}'.format(player['id'])] = \
                forms.MultipleChoiceField(choices=guarenteed_choices,
                                          widget=forms.RadioSelect,
                                          label='{}, {}'.format(player['player'].last_name,
                                                                player['player'].first_name))

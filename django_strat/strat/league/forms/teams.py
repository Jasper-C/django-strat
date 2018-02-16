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


class Renewable(forms.Form):

    def __init__(self, *args, **kwargs):
        player = kwargs.pop('player')
        super(RenewableContract, self).__init__(*args, **kwargs)

        # self.fields['name'] = forms.Field(widget=forms.HiddenInput,
        #                                   label='{}, {}'.format(player['contract'].player.last_name,
        #                                                         player['contract'].player.first_name))
        # self.fields['salary'] = forms.Field(widget=forms.HiddenInput,
        #                                     label='{}'.format(player['contract'].salary))
        # self.fields['contract'] = forms.Field(widget=forms.HiddenInput,
        #                                       label='{}'.format(player['contract'].type))
        self.fields['{}'.format(player['id'])] = \
            forms.MultipleChoiceField(choices=renewable_choices,
                                      widget=forms.RadioSelect,
                                      label='{}, {}'.format(player['contract'].player.last_name,
                                                            player['contract'].player.first_name,))


class RenewableList(forms.Form):

    def __init__(self, *args, **kwargs):
        renewable = kwargs.pop('renewable')
        super(RenewableList, self).__init__(*args, **kwargs)

        for i, player in enumerate(renewable):
            self.fields['name_{}'.format(player['id'])] = \
                forms.Field(widget=forms.HiddenInput,
                            label='{}, {}'.format(player['player'].last_name,
                                                  player['player'].first_name),
                            show_hidden_initial=True)
            self.fields['salary_{}'.format(player['id'])] = \
                forms.Field(widget=forms.HiddenInput,
                            label='{}'.format(player['contract'].salary),
                            show_hidden_initial=True)
            self.fields['contract_{}'.format(player['id'])] = \
                forms.Field(widget=forms.HiddenInput,
                            label='{}'.format(player['contract'].type))
            self.fields['choice_{}'.format(player['id'])] = \
                forms.MultipleChoiceField(choices=renewable_choices,
                                          widget=forms.RadioSelect,
                                          label='{}'.format(player['id']))
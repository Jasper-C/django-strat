import django_tables2 as tables
from django_tables2 import A


class BaseCardStats(tables.Table):
    hits_left = tables.Column(verbose_name='H L', accessor=A('h_l'),
                              order_by=A('-hits_left'),
                              attrs={
                                  'td': {'align': 'Right', 'class': 'Left'},
                                  'th': {'class': 'Left'}
                              })
    onbase_left = tables.Column(verbose_name='OB L', accessor=A('ob_l'),
                                order_by=A('-onbase_left'),
                                attrs={
                                    'td': {'align': 'Right', 'class': 'Left'},
                                    'th': {'class': 'Left'}
                                })
    totalbase_left = tables.Column(verbose_name='TB L', accessor=A('tb_l'),
                                   order_by=A('-totalbase_left'),
                                   attrs={
                                       'td': {'align': 'Right', 'class': 'Left'},
                                       'th': {'class': 'Left'}
                                   })
    homerun_left = tables.Column(verbose_name='HR L', accessor=A('hr_l'),
                                 order_by=A('-homeruns_left'),
                                 attrs={
                                     'td': {'align': 'Right', 'class': 'Left'},
                                     'th': {'class': 'Left'}
                                 })
    ballpark_left = tables.Column(verbose_name='BP L', accessor=A('bp_l'),
                                  order_by=(A('-diamonds_left'), A('-triangles_left')),
                                  attrs={
                                      'td': {'align': 'Center', 'class': 'Left'},
                                      'th': {'class': 'Left'}
                                  })
    gbA_left = tables.Column(verbose_name='dp L', accessor=A('gba_l'),
                             order_by=A('gba_left'),
                             attrs={
                                 'td': {'align': 'Right', 'class': 'Left'},
                                 'th': {'class': 'Left'}
                             })
    hits_right = tables.Column(verbose_name='H R', accessor=A('h_r'),
                               order_by=A('-hits_right'),
                               attrs={
                                   'td': {'align': 'Right', 'class': 'Right'},
                                   'th': {'class': 'Right'}
                               })
    onbase_right = tables.Column(verbose_name='OB R', accessor=A('ob_r'),
                                 order_by=A('-onbase_right'),
                                 attrs={
                                     'td': {'align': 'Right', 'class': 'Right'},
                                     'th': {'class': 'Right'}
                                 })
    totalbase_right = tables.Column(verbose_name='TB R', accessor=A('tb_r'),
                                    order_by=A('-totalbase_right'),
                                    attrs={
                                        'td': {'align': 'Right', 'class': 'Right'},
                                        'th': {'class': 'Right'}
                                    })
    homerun_right = tables.Column(verbose_name='HR R', accessor=A('hr_r'),
                                  order_by=A('-homeruns_right'),
                                  attrs={
                                      'td': {'align': 'Right', 'class': 'Right'},
                                      'th': {'class': 'Right'}
                                  })
    ballpark_right = tables.Column(verbose_name='BP R', accessor=A('bp_r'),
                                   order_by=(A('-diamonds_right'), A('-triangles_right')),
                                   attrs={
                                       'td': {'align': 'Center', 'class': 'Right'},
                                       'th': {'class': 'Right'}
                                   })
    gbA_right = tables.Column(verbose_name='dp R', accessor=A('gba_r'),
                              order_by=A('gba_right'),
                              attrs={
                                  'td': {'align': 'Right', 'class': 'Right'},
                                  'th': {'class': 'Right'}
                              })

    class Meta:
        template_name = 'django_tables2/bootstrap.html'


class BaseHitter(BaseCardStats):
    clutch_left = tables.Column(verbose_name='cl L', accessor=A('cl_l'),
                                order_by=A('-clutch_left'),
                                attrs={
                                    'td': {'align': 'Right', 'class': 'Left'},
                                    'th': {'class': 'Left'}
                                })
    clutch_right = tables.Column(verbose_name='cl R', accessor=A('cl_r'),
                                 order_by=A('-clutch_right'),
                                 attrs={
                                     'td': {'align': 'Right', 'class': 'Right'},
                                     'th': {'class': 'Right'}
                                 })
    defense = tables.Column(verbose_name='Defense', accessor=A('defensive_string'),
                            orderable=False,
                            attrs={
                                'td': {'align': 'Left'},
                            })

    class Meta:
        sequence = (
            'hits_left',
            'onbase_left',
            'totalbase_left',
            'homerun_left',
            'ballpark_left',
            'clutch_left',
            'gbA_left',
            'hits_right',
            'onbase_right',
            'totalbase_right',
            'homerun_right',
            'ballpark_right',
            'clutch_right',
            'gbA_right',
            'defense'
        )


class SingleHitter(BaseHitter):
    year = tables.columns.Column(verbose_name='Year', accessor=A('year'),
                                 order_by=A('-year'),
                                 attrs={
                                     'td': {'align': 'Right'},
                                 })

    class Meta:
        sequence = (
            'year',
            'hits_left',
            'onbase_left',
            'totalbase_left',
            'homerun_left',
            'ballpark_left',
            'clutch_left',
            'gbA_left',
            'hits_right',
            'onbase_right',
            'totalbase_right',
            'homerun_right',
            'ballpark_right',
            'clutch_right',
            'gbA_right',
            'defense'
        )


class TeamHitter(BaseHitter):
    player = tables.columns.LinkColumn(verbose_name='Name', viewname='league:player_detail',
                                       args=[A('display_name')],
                                       text=lambda x: x.display_name())

    class Meta:
        sequence = (
            'player',
            'hits_left',
            'onbase_left',
            'totalbase_left',
            'homerun_left',
            'ballpark_left',
            'clutch_left',
            'gbA_left',
            'hits_right',
            'onbase_right',
            'totalbase_right',
            'homerun_right',
            'ballpark_right',
            'clutch_right',
            'gbA_right',
            'defense'
        )


class MultiTeamHitter(TeamHitter):
    team = tables.columns.Column(verbose_name='Team')

    class Meta:
        sequence = (
            'player',
            'team',
            '...'
        )


class BasePitcher(BaseCardStats):
    starter = tables.Column(verbose_name='S', accessor=A('starter_endurance'),
                            order_by=(A('-starter_endurance')),
                            attrs={
                                'td': {'align': 'Center'},
                            })
    relief = tables.Column(verbose_name='R', accessor=A('relief_endurance'),
                           order_by=(A('-relief_endurance')),
                           attrs={
                               'td': {'align': 'Center'},
                           })
    closer = tables.Column(verbose_name='C', accessor=A('closer_display'),
                           order_by=(A('-closer_rating')),
                           attrs={
                               'td': {'align': 'Center'},
                           })
    hold = tables.Column(verbose_name='Hld', accessor=A('hold_rating'),
                         order_by=(A('hold')),
                         attrs={
                             'td': {'align': 'Right'},
                         })
    wild_pitch = tables.Column(verbose_name='WP', accessor=A('wild_pitch'),
                               order_by=(A('wild_pitch')),
                               attrs={
                                   'td': {'align': 'Right'},
                               })
    balk = tables.Column(verbose_name='Bk', accessor=A('balk'),
                         order_by=(A('balk')),
                         attrs={
                             'td': {'align': 'Right'},
                         })
    defense = tables.Column(verbose_name='Defense', accessor=A('defense'),
                            order_by=(A('def_range'), A('def_error')),
                            attrs={
                                'td': {'align': 'Right'},
                            })
    phc = tables.Column(verbose_name='PHC', accessor=A('phc'),
                        order_by=(A('-pitcher_hitting_card'), A('bunt_rating')),
                        attrs={
                            'td': {'align': 'Center'},
                        })

    class Meta:
        sequence = (
            'hits_left',
            'onbase_left',
            'totalbase_left',
            'homerun_left',
            'ballpark_left',
            'gbA_left',
            'hits_right',
            'onbase_right',
            'totalbase_right',
            'homerun_right',
            'ballpark_right',
            'gbA_right',
        )


class SinglePitcher(BasePitcher):
    year = tables.columns.Column(verbose_name='Year', accessor=A('year'),
                                 order_by=A('-year'),
                                 attrs={
                                     'td': {'align': 'Right'},
                                 })

    class Meta:
        sequence = (
            'year',
            '...'
        )


class TeamPitcher(BasePitcher):
    player = tables.columns.LinkColumn(verbose_name='Name', viewname='league:player_detail',
                                       args=[A('display_name')],
                                       text=lambda x: x.display_name())

    class Meta:
        sequence = (
            'player',
            '...',
        )


class MultiTeamPitcher(TeamPitcher):
    pass
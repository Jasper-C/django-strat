# Generated by Django 2.0 on 2017-12-21 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballpark',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=75)),
                ('location', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('singles_left', models.IntegerField()),
                ('singles_right', models.IntegerField()),
                ('homeruns_left', models.IntegerField()),
                ('homeruns_right', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=8)),
                ('year', models.IntegerField(default=1)),
                ('contract_season', models.IntegerField(default=1)),
                ('length', models.IntegerField()),
                ('salary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(db_column='current_owner', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('money', models.IntegerField()),
                ('note', models.TextField()),
                ('paying', models.ForeignKey(db_column='paying', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paying', to='league.Franchise')),
                ('receiving', models.ForeignKey(db_column='receiving', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiving', to='league.Franchise')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('player_type', models.CharField(max_length=2)),
                ('active', models.BooleanField(default=True)),
                ('bats', models.CharField(max_length=1)),
                ('throws', models.CharField(max_length=1)),
                ('birth_year', models.IntegerField()),
                ('bbref_id', models.CharField(max_length=20)),
                ('mlb_id', models.CharField(max_length=10)),
                ('bp_id', models.CharField(max_length=10)),
                ('cbs_id', models.CharField(max_length=10)),
                ('espn_id', models.CharField(max_length=10)),
                ('fg_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(db_column='player', on_delete=django.db.models.deletion.PROTECT, to='league.Player')),
                ('team', models.ForeignKey(db_column='team', on_delete=django.db.models.deletion.PROTECT, to='league.Franchise')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('abbreviation', models.CharField(max_length=5)),
                ('location', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('division', models.CharField(choices=[('ALW', 'AL West'), ('ALE', 'AL East'), ('NLW', 'NL West'), ('NLE', 'NL East')], max_length=12)),
                ('ballpark', models.ForeignKey(db_column='ballpark', on_delete=django.db.models.deletion.PROTECT, to='league.Ballpark')),
                ('franchise', models.ForeignKey(db_column='franchise', on_delete=django.db.models.deletion.CASCADE, to='league.Franchise')),
                ('owner', models.ForeignKey(db_column='owner', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='player',
            field=models.ForeignKey(db_column='player_id', on_delete=django.db.models.deletion.CASCADE, to='league.Player'),
        ),
    ]

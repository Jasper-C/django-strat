# Generated by Django 2.0 on 2017-12-21 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roster',
            name='player',
        ),
        migrations.RemoveField(
            model_name='roster',
            name='team',
        ),
        migrations.AddField(
            model_name='contract',
            name='team',
            field=models.ForeignKey(db_column='team', default='EVT', on_delete=django.db.models.deletion.PROTECT, to='league.Franchise'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Roster',
        ),
    ]
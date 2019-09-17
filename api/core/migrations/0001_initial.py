# Generated by Django 2.2.5 on 2019-09-19 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_num', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('match_id', 'game_num'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('duration', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('-start_time',),
            },
        ),
        migrations.CreateModel(
            name='MatchConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_of', models.PositiveSmallIntegerField()),
                ('extended_mode', models.BooleanField()),
                ('public', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='PlayerMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_num', models.IntegerField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Player')),
            ],
            options={
                'ordering': ('player_num',),
                'abstract': False,
                'unique_together': {('player_num', 'match'), ('player', 'match')},
            },
        ),
        migrations.CreateModel(
            name='PlayerGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_num', models.IntegerField()),
                ('move', models.CharField(choices=[('rock', 'rock'), ('paper', 'paper'), ('scissors', 'scissors'), ('lizard', 'lizard'), ('spock', 'spock')], max_length=20)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Player')),
            ],
            options={
                'ordering': ('player_num',),
                'abstract': False,
                'unique_together': {('player_num', 'game'), ('player', 'game')},
            },
        ),
        migrations.AddField(
            model_name='match',
            name='config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.MatchConfig'),
        ),
        migrations.AddField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(related_name='matches', through='core.PlayerMatch', to='core.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='rematch',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent', to='core.Match'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='match_wins', to='core.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='core.Match'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(through='core.PlayerGame', to='core.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='game_wins', to='core.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('game_num', 'match')},
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-16 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livematch', '0005_livematch_rematch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='liveplayermatch',
            options={'ordering': ('id',)},
        ),
    ]
# Generated by Django 2.2.3 on 2019-08-09 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livematch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='livematch',
            name='best_of',
            field=models.PositiveSmallIntegerField(default=5),
        ),
    ]

# Generated by Django 2.2.4 on 2019-08-22 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livematch', '0003_auto_20190822_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livematch',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
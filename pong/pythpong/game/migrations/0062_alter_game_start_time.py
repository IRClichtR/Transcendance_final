# Generated by Django 5.0.7 on 2024-07-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0061_alter_game_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.IntegerField(default=1721908199),
        ),
    ]

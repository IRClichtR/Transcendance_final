# Generated by Django 5.0.7 on 2024-08-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0056_alter_game_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.IntegerField(default=1722603631),
        ),
    ]

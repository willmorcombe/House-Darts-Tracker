# Generated by Django 5.1.5 on 2025-01-29 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_alter_gamestatistics_unique_together_game_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamestatistics',
            name='number_of_throws',
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='best_of_legs',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='best_of_sets',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

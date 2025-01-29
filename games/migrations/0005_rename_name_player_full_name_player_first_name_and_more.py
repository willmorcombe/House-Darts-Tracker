# Generated by Django 5.1.5 on 2025-01-26 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_gamestatistics_delete_gamestatehistory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='full_name',
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]

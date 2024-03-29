# Generated by Django 4.0.4 on 2022-06-28 23:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0003_character_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='exp',
        ),
        migrations.AlterField(
            model_name='character',
            name='clss',
            field=models.IntegerField(choices=[(12, 'Barbarian'), (8, 'Bard'), (8, 'Cleric'), (8, 'Druid'), (10, 'Fighter'), (8, 'Monk'), (10, 'Paladin'), (10, 'Ranger'), (8, 'Rogue'), (6, 'Sorcerer'), (8, 'Warlock'), (6, 'Wizard')], default=False),
        ),
        migrations.AlterField(
            model_name='character',
            name='level',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
    ]

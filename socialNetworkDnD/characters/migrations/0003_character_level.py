# Generated by Django 4.0.4 on 2022-06-28 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_rename_descrizione_fisica_character_fisical_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='level',
            field=models.IntegerField(default=False),
        ),
    ]

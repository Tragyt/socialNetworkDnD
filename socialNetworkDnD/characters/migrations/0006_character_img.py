# Generated by Django 4.0.4 on 2022-06-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0005_remove_character_hitdice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='img',
            field=models.ImageField(blank=True, default='/static/images/download.png', upload_to='images/'),
        ),
    ]
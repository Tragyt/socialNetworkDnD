# Generated by Django 4.0.4 on 2022-06-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnd', '0011_alter_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='static/'),
        ),
    ]

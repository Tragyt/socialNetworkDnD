# Generated by Django 4.0.4 on 2022-07-06 04:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0007_alter_evaluation_user_alter_evaluation_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='value',
            field=models.IntegerField(blank=True, choices=[(0, 'Positive'), (1, 'Negative'), (2, 'None')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 6, 4, 54, 18, 367235, tzinfo=utc)),
        ),
    ]
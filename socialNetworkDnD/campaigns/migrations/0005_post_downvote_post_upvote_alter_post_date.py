# Generated by Django 4.0.4 on 2022-07-06 03:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_alter_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downvote',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 6, 3, 11, 22, 65001, tzinfo=utc)),
        ),
    ]

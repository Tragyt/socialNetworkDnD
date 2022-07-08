from datetime import date, datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from characters.models import Character
from dnd.models import Profile

EVAL = (
    (0, "Positive"),
    (1, "Negative"),
    (2, "None")
)


class Campaign(models.Model):
    master = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    characters = models.ManyToManyField(Character, default=None)


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    img = models.ImageField(upload_to='images/', default=None, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateTimeField(default=None)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)


class Evaluation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    value = models.IntegerField(choices=EVAL, blank=True)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    Profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(default=None)

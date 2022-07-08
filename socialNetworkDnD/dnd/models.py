from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from characters.models import Character

FRIENDSHIP_STATUS = (
    (True, "Friends"),
    (False, "Not yet")
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default=None, null=True, blank=True)
    img = models.ImageField(upload_to='images/', default="images/download.png", blank=True)
    experience = models.CharField(max_length=500, default=None, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="utente_richiesta")
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="utente_accettazione")
    status = models.CharField(choices=FRIENDSHIP_STATUS, max_length=20, default=False)


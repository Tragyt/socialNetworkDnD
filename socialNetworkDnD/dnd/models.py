from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

FRIENDSHIP_STATUS = (
    (True, "Friends"),
    (False, "Not yet")
)


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    classe = models.CharField(max_length=50)
    razza = models.CharField(max_length=50)
    allineamento = models.CharField(max_length=50)
    esperienza = models.IntegerField()
    descrizione_fisica = models.CharField(max_length=500)
    descrizione_personalità = models.CharField(max_length=500)
    Hp = models.IntegerField()
    AC = models.IntegerField()
    Initiative = models.IntegerField()
    Speed = models.IntegerField()
    passivePerception = models.IntegerField()
    proficientyBonus = models.IntegerField()
    HitDice = models.IntegerField()
    strenght = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
    acrobatics = models.IntegerField()
    medicine = models.IntegerField()
    animalHandling = models.IntegerField()
    nature = models.IntegerField()
    arcana = models.IntegerField()
    perception = models.IntegerField()
    athletics = models.IntegerField()
    performance = models.IntegerField()
    deception = models.IntegerField()
    persuasion = models.IntegerField()
    history = models.IntegerField()
    religion = models.IntegerField()
    insight = models.IntegerField()
    sleightOfHand = models.IntegerField()
    intimidation = models.IntegerField()
    stealth = models.IntegerField()
    investigation = models.IntegerField()
    survival = models.IntegerField()
    feats = models.CharField(max_length=500)
    armor = models.CharField(max_length=500)
    weapons = models.CharField(max_length=500)
    equipment = models.CharField(max_length=500)
    CP = models.IntegerField()
    SP = models.IntegerField()
    EP = models.IntegerField()
    GP = models.IntegerField()
    PP = models.IntegerField()
    SpellSlots1 = models.IntegerField()
    SpellSlots2 = models.IntegerField()
    SpellSlots3 = models.IntegerField()
    SpellSlots4 = models.IntegerField()
    SpellSlots5 = models.IntegerField()
    SpellSlots6 = models.IntegerField()
    SpellSlots7 = models.IntegerField()
    SpellSlots8 = models.IntegerField()
    SpellSlots9 = models.IntegerField()
    spells = models.CharField(max_length=500)


class Campaign(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    characters = models.ManyToManyField(Character, default=None)
    # immagine


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default=None, null=True, blank=True)
    img = models.ImageField(upload_to='images/', default="/static/images/download.png", blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friendship(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="utente_richiesta")
    user2 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="utente_accettazione")
    status = models.CharField(choices=FRIENDSHIP_STATUS, max_length=20, default=False)


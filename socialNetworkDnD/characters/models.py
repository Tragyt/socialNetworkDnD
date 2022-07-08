from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

CLASSES = (
    (12, "Barbarian"),
    (8, "Bard"),
    (8, "Cleric"),
    (8, "Druid"),
    (10, "Fighter"),
    (8, "Monk"),
    (10, "Paladin"),
    (10, "Ranger"),
    (8, "Rogue"),
    (6, "Sorcerer"),
    (8, "Warlock"),
    (6, "Wizard")
)

RACES = (
    (0, "Dwarf"),
    (1, "Elf"),
    (2, "Halfling"),
    (3, "Human"),
    (4, "Dragonborn"),
    (5, "Gnome"),
    (6, "Half-Elf"),
    (7, "Half-Orc"),
    (8, "Tiefling")
)

ALIGNMENTS = (
    (0, "Lawful Good"),
    (1, "Neutral Good"),
    (2, "Chaotic Good"),
    (3, "Lawful Neutral"),
    (4, "True Neutral"),
    (5, "Chaotic Neutral"),
    (6, "Lawful Evil"),
    (7, "Neutral Evil"),
    (8, "Chaotic Evil")
)

WEAPON_TYPES = (
    (0, "Simple Melee"),
    (1, "Simple Ranged"),
    (2, "Martial Melee"),
    (3, "Martial Ranged")
)

ABILITIES = (
    (0, "Strength"),
    (1, "Dexterity"),
    (2, "Constitution"),
    (3, "Intelligence"),
    (4, "Wisdom"),
    (5, "Charisma")
)


class Character(models.Model):
    public = models.BooleanField(default=True)

    img = models.ImageField(upload_to='images/', default="images/download.png", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    clss = models.IntegerField(choices=CLASSES, default=False)
    race = models.IntegerField(choices=RACES, default=False)
    alignment = models.IntegerField(choices=ALIGNMENTS, default=False)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=1)
    fisical_description = models.CharField(max_length=500, default=None, null=True, blank=True)
    personality_traits = models.CharField(max_length=500, default=None, null=True, blank=True)
    Hp = models.IntegerField(default=1)
    AC = models.IntegerField(default=1)
    Initiative = models.IntegerField(default=1)
    Speed = models.IntegerField(default=30)
    proficientyBonus = models.IntegerField(default=1)

    strenght = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=8)
    dexterity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=8)
    constitution = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=8)
    intelligence = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=8)
    wisdom = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=8)
    charisma = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=8)

    saving_strenght = models.IntegerField(default=0)
    saving_dexterity = models.IntegerField(default=0)
    saving_constitution = models.IntegerField(default=0)
    saving_intelligence = models.IntegerField(default=0)
    saving_wisdom = models.IntegerField(default=0)
    saving_charisma = models.IntegerField(default=0)

    acrobatics = models.IntegerField(default=1)
    medicine = models.IntegerField(default=1)
    animalHandling = models.IntegerField(default=1)
    nature = models.IntegerField(default=1)
    arcana = models.IntegerField(default=1)
    perception = models.IntegerField(default=1)
    athletics = models.IntegerField(default=1)
    performance = models.IntegerField(default=1)
    deception = models.IntegerField(default=1)
    persuasion = models.IntegerField(default=1)
    history = models.IntegerField(default=1)
    religion = models.IntegerField(default=1)
    insight = models.IntegerField(default=1)
    sleightOfHand = models.IntegerField(default=1)
    intimidation = models.IntegerField(default=1)
    stealth = models.IntegerField(default=1)
    investigation = models.IntegerField(default=1)
    survival = models.IntegerField(default=1)

    passivePerception = models.IntegerField(default=1)
    feats = models.CharField(max_length=500, default=None, null=True, blank=True)
    armor = models.CharField(max_length=500, default=None, null=True, blank=True)
    weapons = models.CharField(max_length=500, default=None, null=True, blank=True)

    CP = models.IntegerField(default=0)
    SP = models.IntegerField(default=0)
    EP = models.IntegerField(default=0)
    GP = models.IntegerField(default=0)
    PP = models.IntegerField(default=0)


class Proficiencies(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    saving_strenght = models.BooleanField(default=False)
    saving_dexterity = models.BooleanField(default=False)
    saving_constitution = models.BooleanField(default=False)
    saving_intelligence = models.BooleanField(default=False)
    saving_wisdom = models.BooleanField(default=False)
    saving_charisma = models.BooleanField(default=False)

    acrobatics = models.BooleanField(default=False)
    medicine = models.BooleanField(default=False)
    animalHandling = models.BooleanField(default=False)
    nature = models.BooleanField(default=False)
    arcana = models.BooleanField(default=False)
    perception = models.BooleanField(default=False)
    athletics = models.BooleanField(default=False)
    performance = models.BooleanField(default=False)
    deception = models.BooleanField(default=False)
    persuasion = models.BooleanField(default=False)
    history = models.BooleanField(default=False)
    religion = models.BooleanField(default=False)
    insight = models.BooleanField(default=False)
    sleightOfHand = models.BooleanField(default=False)
    intimidation = models.BooleanField(default=False)
    stealth = models.BooleanField(default=False)
    investigation = models.BooleanField(default=False)
    survival = models.BooleanField(default=False)


class Weapon(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    type = models.IntegerField(choices=WEAPON_TYPES)
    ability = models.IntegerField(choices=ABILITIES)
    attackBonus = models.IntegerField(default=0)
    damage = models.CharField(default="1 D4", max_length=50)


class Equipment(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)


class Abilities(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    effect = models.CharField(max_length=255)
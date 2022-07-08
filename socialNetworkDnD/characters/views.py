from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from characters.forms import CharacterCreateForm, UpdateCharForm
from characters.models import Character, Proficiencies, Weapon, Equipment, Abilities
from dnd.models import Profile
from socialNetworkDnD.views import new_requests, list_friends, list_characters, UpdateBaseView, CreateBaseView, \
    get_context


class CharacterCreate(CreateBaseView):
    model = Character
    form_class = CharacterCreateForm
    success_url = "dnd:home"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        if obj.race == 0:
            obj.constitution += 2
            obj.Speed = 25
        elif obj.race == 1:
            obj.dexterity += 2
        elif obj.race == 2:
            obj.dexterity += 2
            obj.Speed = 25
        elif obj.race == 3:
            obj.dexterity += 1
            obj.strenght += 1
            obj.constitution += 1
            obj.intelligence += 1
            obj.wisdom += 1
            obj.charisma += 1
        elif obj.race == 4:
            obj.strenght += 2
        elif obj.race == 5:
            obj.intelligence += 2
            obj.Speed = 25
        elif obj.race == 6:
            obj.charisma += 2
        elif obj.race == 7:
            obj.strenght += 2
        elif obj.race == 8:
            obj.charisma += 2

        constitution = (obj.constitution - 10) / 2
        dexterity = (obj.dexterity - 10) / 2
        wisdom = (obj.wisdom - 10) / 2
        intelligence = (obj.intelligence - 10) / 2
        strenght = (obj.strenght - 10) / 2
        charisma = (obj.charisma - 10) / 2

        obj.Hp = obj.clss + constitution + (((obj.clss + 2) / 2) + constitution) * (
                obj.level - 1)
        obj.AC = 10 + dexterity
        obj.Initiative = dexterity
        obj.proficientyBonus = 2 + (obj.level - 1) / 4

        obj.saving_strenght = strenght
        obj.saving_dexterity = dexterity
        obj.saving_constitution = constitution
        obj.saving_intelligence = intelligence
        obj.saving_wisdom = wisdom
        obj.saving_charisma = charisma

        obj.acrobatics = dexterity
        obj.medicine = wisdom
        obj.animalHandling = wisdom
        obj.nature = intelligence
        obj.arcana = intelligence
        obj.perception = wisdom
        obj.athletics = strenght
        obj.performance = charisma
        obj.deception = charisma
        obj.persuasion = charisma
        obj.history = intelligence
        obj.religion = intelligence
        obj.insight = wisdom
        obj.sleightOfHand = dexterity
        obj.intimidation = charisma
        obj.stealth = dexterity
        obj.investigation = intelligence
        obj.survival = wisdom

        obj.passivePerception = 10 + obj.perception

        obj.save()
        Proficiencies.objects.create(character=obj)
        return HttpResponseRedirect("/dnd/home")


@login_required
def character_sheet(request):
    profile = get_object_or_404(Profile, user=request.user.pk)
    if request.method == 'POST':
        character_name = request.POST["name"]
        character = get_object_or_404(Character, user_id=profile.user_id, name=character_name)
        return redirect("sheet_view", character.pk)


class CharacterSheet(LoginRequiredMixin, ListView):
    model = Character
    template_name = "character.html"
    pk = None

    def get_queryset(self):
        self.pk = self.request.resolver_match.kwargs["pk"]
        result = Character.objects.get(pk=self.pk)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context(self, context)

        context["proficiencies"] = Proficiencies.objects.get(character_id=self.pk)
        context["weapons"] = Weapon.objects.filter(character_id=self.pk)
        context["equipment"] = Equipment.objects.filter(character_id=self.pk)
        context["abilities"] = Abilities.objects.filter(character_id=self.pk)

        return context


class UpdateCharacter(UpdateBaseView):
    model = Character
    form_class = UpdateCharForm
    pk = None

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk

        item.saving_constitution = (item.constitution - 10) / 2
        item.saving_dexterity = (item.dexterity - 10) / 2
        item.saving_wisdom = (item.wisdom - 10) / 2
        item.saving_intelligence = (item.intelligence - 10) / 2
        item.saving_strenght = (item.strenght - 10) / 2
        item.saving_charisma = (item.charisma - 10) / 2

        item.AC = 10 + item.saving_dexterity
        item.Initiative = item.saving_dexterity

        item.acrobatics = item.saving_dexterity
        item.medicine = item.saving_wisdom
        item.animalHandling = item.saving_wisdom
        item.nature = item.saving_intelligence
        item.arcana = item.saving_intelligence
        item.perception = item.saving_wisdom
        item.athletics = item.saving_strenght
        item.performance = item.saving_charisma
        item.deception = item.saving_charisma
        item.persuasion = item.saving_charisma
        item.history = item.saving_intelligence
        item.religion = item.saving_intelligence
        item.insight = item.saving_wisdom
        item.sleightOfHand = item.saving_dexterity
        item.intimidation = item.saving_charisma
        item.stealth = item.saving_dexterity
        item.investigation = item.saving_intelligence
        item.survival = item.saving_wisdom

        item.passivePerception = 10 + item.perception

        return super(UpdateCharacter, self).form_valid(form)

    def get_success_url(self):
        return reverse('sheet_view', kwargs={'pk': self.pk})


class UpdateProficienciesSavings(UpdateBaseView):
    model = Proficiencies
    fields = ("saving_strenght", "saving_dexterity", "saving_constitution", "saving_intelligence", "saving_wisdom",
              "saving_charisma")

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs["char"]
        return reverse('sheet_view', kwargs={'pk': pk})


class UpdateProficienciesSkills(UpdateBaseView):
    model = Proficiencies
    fields = ("acrobatics", "medicine", "animalHandling", "nature", "arcana",
              "perception", "athletics", "performance", "deception", "persuasion", "history", "religion", "insight",
              "sleightOfHand", "intimidation", "stealth", "investigation", "survival")

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs["char"]
        return reverse('sheet_view', kwargs={'pk': pk})


class AddWeapon(CreateBaseView):
    model = Weapon
    fields = ("name", "description", "type", "ability", "damage")

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs["char"]
        return reverse('sheet_view', kwargs={'pk': pk})

    def form_valid(self, form):
        obj = form.save(commit=False)
        pk = self.request.resolver_match.kwargs["char"]
        obj.character = Character.objects.get(pk=pk)

        if obj.ability == 0:
            obj.attackBonus = (obj.character.strenght - 10) / 2 + obj.character.proficientyBonus
        elif obj.ability == 1:
            obj.attackBonus = (obj.character.dexterity - 10) / 2 + obj.character.proficientyBonus
        elif obj.ability == 2:
            obj.attackBonus = (obj.character.constitution - 10) / 2 + obj.character.proficientyBonus
        elif obj.ability == 3:
            obj.attackBonus = (obj.character.intelligence - 10) / 2 + obj.character.proficientyBonus
        elif obj.ability == 4:
            obj.attackBonus = (obj.character.wisdom - 10) / 2 + obj.character.proficientyBonus
        elif obj.ability == 5:
            obj.attackBonus = (obj.character.charisma - 10) / 2 + obj.character.proficientyBonus

        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class AddEquipment(CreateBaseView):
    model = Equipment
    fields = ("name", "description")

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs["char"]
        return reverse('sheet_view', kwargs={'pk': pk})

    def form_valid(self, form):
        obj = form.save(commit=False)
        pk = self.request.resolver_match.kwargs["char"]
        obj.character = Character.objects.get(pk=pk)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def delete_weapon(request, pk, char):
    Weapon.objects.get(pk=pk).delete()
    return redirect("sheet_view", char)


@login_required
def delete_equipment(request, pk, char):
    Equipment.objects.get(pk=pk).delete()
    return redirect("sheet_view", char)


class UpdateMoney(UpdateBaseView):
    model = Character
    fields = ("CP", "SP", "EP", "GP", "PP")

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs["pk"]
        return reverse('sheet_view', kwargs={'pk': pk})


class AddAbility(CreateBaseView):
    model = Abilities
    fields = ("name", "effect")

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs["char"]
        return reverse('sheet_view', kwargs={'pk': pk})

    def form_valid(self, form):
        obj = form.save(commit=False)
        pk = self.request.resolver_match.kwargs["char"]
        obj.character = Character.objects.get(pk=pk)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def delete_ability(request, pk, char):
    Abilities.objects.get(pk=pk).delete()
    return redirect("sheet_view", char)


@login_required
def level_up(request, pk):
    character = Character.objects.get(pk=pk)
    character.level += 1
    character.Hp += ((character.clss + 2) / 2) + character.saving_constitution
    character.proficientyBonus = 2 + (character.level - 1) / 4
    character.save()
    return redirect("sheet_view", pk)


@login_required
def delete_character(request, pk):
    Character.objects.get(id=pk).delete()
    return redirect('home')

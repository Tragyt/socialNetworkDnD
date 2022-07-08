from django import forms
from characters.models import Character, Weapon


class CharacterCreateForm(forms.ModelForm):
    fisical_description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}), required=False)

    personality_traits = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}), required=False)

    class Meta:
        model = Character
        fields = ("name", "clss", "race", "alignment", "level", "fisical_description", "personality_traits", "strenght",
                  "dexterity", "constitution", "intelligence", "wisdom", "charisma", "CP", "SP", "EP", "GP", "PP",
                  "public")


class UpdateCharForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3"}), required=False)
    img = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Character
        fields = ("name", "img", "strenght", "dexterity", "constitution", "intelligence", "wisdom", "charisma",
                  "fisical_description", "personality_traits", "public")

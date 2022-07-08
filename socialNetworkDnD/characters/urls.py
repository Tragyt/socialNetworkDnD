from django.urls import path

from characters.views import CharacterCreate, CharacterSheet, character_sheet, UpdateCharacter, \
    UpdateProficienciesSavings, \
    UpdateProficienciesSkills, AddWeapon, delete_weapon, AddEquipment, delete_equipment, UpdateMoney, AddAbility, \
    delete_ability, level_up, delete_character

urlpatterns = [
    path("create/", CharacterCreate.as_view(), name="create"),
    path("sheet/", character_sheet, name="sheet"),
    path("sheet_view/<pk>/", CharacterSheet.as_view(), name="sheet_view"),
    path("updateimg/<pk>", UpdateCharacter.as_view(), name="update_img"),
    path("updatesavings/<pk><char>", UpdateProficienciesSavings.as_view(), name="update_savings"),
    path("updateskills/<pk><char>", UpdateProficienciesSkills.as_view(), name="update_skills"),
    path("addweapon/<char>", AddWeapon.as_view(), name="add_weapon"),
    path("rmweapon/<pk><char>", delete_weapon, name="rmv_weapon"),
    path("addequipment/<char>", AddEquipment.as_view(), name="add_equipment"),
    path("rmequipment/<pk><char>", delete_equipment, name="rmv_equipment"),
    path("updatemoney/<pk>", UpdateMoney.as_view(), name="update_money"),
    path("addability/<char>", AddAbility.as_view(), name="add_ability"),
    path("rmability/<pk><char>", delete_ability, name="rmv_ability"),
    path("lvlup/<pk>", level_up, name="level_up"),
    path("deletecharacter/<pk>", delete_character, name="delete_character")
]

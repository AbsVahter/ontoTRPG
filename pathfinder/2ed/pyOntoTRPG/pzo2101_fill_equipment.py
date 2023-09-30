import pandas as pd
from owlready2 import *
import main
import pzo2101_fill_traits


def fill_shield(pzo2101):
    with pzo2101:
        class Shield(pzo2101.Defense_equipment):
            comment = ("A shield can increase your character’s defense beyond the protection their armor provides. "
                       "Your character must be wielding a shield in one hand to make use of it, and it grants its "
                       "bonus to AC only if they use an action to Raise a Shield. This action grants the shield’s "
                       "bonus to AC as a circumstance bonus until their next turn starts. A shield’s Speed penalty "
                       "applies whenever your character is holding the shield, whether they have raised it or not.")
        main.fill_onto_from_xml(pzo2101, "Shields", Shield)


def fill_gear(pzo2101):
    with pzo2101:
        class Gear_and_services(pzo2101.Equipment):
            comment = ("Your character needs all sorts of items both while exploring and in downtime, ranging from "
                       "rations to climbing gear to fancy clothing, depending on the situation.")
        main.fill_onto_from_xml(pzo2101, "Adventuring gear", Gear_and_services)

        for index, row in main.read_text_for_parse("Adventuring_gear_corpus"):
            corpus = row['corpus']
            lst_corpus = corpus.split(":")
            for i in range(1, len(lst_corpus)):
                lst_before = lst_corpus[i-1].strip().split(".")
                lst = lst_corpus[i].strip().split(".")
                g_name = lst_before[-1].strip()
                g = pzo2101[main.prepare_name(g_name)]
                g.comment.append(f"{''.join(lst[0:-1])}.")


def fill_packs(pzo2101):
    with pzo2101:
        Equipment = pzo2101.Equipment
        class Equipment_pack(Equipment): pass
        class contains(Equipment_pack >> Equipment): pass
        class Starter_kit(Equipment_pack): pass

        main.fill_onto_from_xml(pzo2101, 'Equipment packs', Equipment_pack)
        Starter_kit.contains.append(pzo2101[main.prepare_name("Adventurer’s pack")])

def fill(pzo2101: Ontology):
    with pzo2101:
        class Equipment(Thing):
            comment = ("To make your mark on the world, you’ll need to have the right equipment, including armor, "
                       "weapons, and other gear. The various equipment that you can purchase during character "
                       "creation. You can usually find these items for sale in most cities and other large "
                       "settlements.")

        class price(Equipment >> str, FunctionalProperty): pass

        class bulk(Equipment >> str, FunctionalProperty):
            comment = ("As a general rule, an item that weighs 5 to 10 pounds is 1 Bulk, an item weighing less than a "
                       "few ounces is negligible, and anything in between is light. Particularly awkward or unwieldy "
                       "items might have higher Bulk values.")

        class hardness(Equipment >> int, FunctionalProperty): pass

        Equipment("coin", price = "100 cp = 10 sp = 1 gp = 1/10 pp",
                  bulk = "A thousand coins of any denomination or combination of denominations count as 1 Bulk.")

        class Defense_equipment(Equipment): pass
        class ac_bonus(Defense_equipment >> int, FunctionalProperty):
            comment = ("This number is the item bonus you add for the armor when determining Armor Class. A shield "
                       "grants a circumstance bonus to AC, but only when the shield is raised.")
        class speed_penalty(Defense_equipment >> int, FunctionalProperty): pass
        class hands(Equipment >> int, FunctionalProperty):
            comment = "Some weapons require one hand to wield, and others require two."

    fill_armor(pzo2101)
    fill_shield(pzo2101)
    fill_weapon(pzo2101)
    fill_weapon_groups(pzo2101)
    fill_gear(pzo2101)
    fill_packs(pzo2101)


def fill_weapon_groups(pzo2101):
    with pzo2101:
        Weapon_by_group = pzo2101.Weapon_by_group
        for trait in pzo2101.Specialization_effect.instances():
            if any([trait in w.has_trait for w in pzo2101.Weapon.instances()]):
                cl = types.new_class(trait.name.split("_trait")[0].capitalize() + "_group", (Weapon_by_group,))
                cl.defined_class = True
                cl.has_trait = trait

        pzo2101.Axe_group.is_a.extend([
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('slashing')]),
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('sweep')]),
        ])
        pzo2101.Bow_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('piercing')]))
        pzo2101.Brawling_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('agile')]))
        pzo2101.Club_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('bludgeoning')]))
        pzo2101.Dart_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('piercing')]))
        pzo2101.Hammer_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('bludgeoning')]))
        pzo2101.Knife_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('agile')]))
        pzo2101.Pick_group.is_a.extend([
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('piercing')]),
        ])
        pzo2101.Sling_group.is_a.extend([
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('bludgeoning')]),
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('propulsive')]),
        ])
        pzo2101.Spear_group.is_a.append(
            pzo2101.has_trait.value(pzo2101[pzo2101_fill_traits.prepare_trait_name('piercing')]))


def fill_weapon(pzo2101: Ontology):
    with pzo2101:
        Equipment = pzo2101.Equipment
        class Weapon(Equipment):
            comment = ("Most characters in Pathfinder carry weapons, ranging from mighty warhammers to graceful bows "
                       "to even simple clubs.")

        class Ammunition(Equipment): pass
        class ammunition(Weapon >> Ammunition, FunctionalProperty): pass
        main.fill_onto_from_xml(pzo2101, "Ammunition", Ammunition)

        class Weapon_by_complexity(Weapon): pass
        class damage(Weapon >> str, FunctionalProperty): pass
        class range(Weapon >> int, FunctionalProperty): pass
        class reload(Weapon >> int, FunctionalProperty):
            comment = ("While all weapons need some amount of time to get into position, many ranged weapons also need "
                       "to be loaded and reloaded. This entry indicates how many Interact actions it takes to reload "
                       "such weapons.")

        class Weapon_by_group(pzo2101.Weapon): pass

        main.fill_onto_from_xml(pzo2101, "Weapons", Weapon_by_complexity)
        for weapon in Weapon.instances():
            weapon.is_a.append(Weapon_by_group)



def fill_armor(pzo2101: Ontology):
    with pzo2101:
        class Armor(pzo2101.Defense_equipment):
            comment = ("Armor increases your character’s defenses, but some medium or heavy armor can hamper movement. "
                       "If you want to increase your character’s defense beyond the protection your armor provides, "
                       "they can use a shield. Armor protects your character only while they’re wearing it.")

        class dex_cap(Armor >> int, FunctionalProperty):
            comment = ("This number is the maximum amount of your Dexterity modifier that can apply to your AC while "
                       "you are wearing a given suit of armor.")

        class check_penalty(Armor >> int, FunctionalProperty):
            comment = ("While wearing your armor, you take this penalty to Strength- and Dexterity-based skill checks, "
                       "except for those that have the attack trait. If you meet the armor’s Strength threshold, "
                       "you don’t take this penalty.")

        class str_threshold(Armor >> int, FunctionalProperty):
            comment = ("This entry indicates the Strength score at which you are strong enough to overcome some of the "
                       "armor’s penalties. If your Strength is equal to or greater than this value, you no longer "
                       "take the armor’s check penalty, and you decrease the Speed penalty by 5 feet")

        main.fill_onto_from_xml(pzo2101, "Armor", Armor)
        for armor in Armor.instances():
            traits = armor.has_trait
            if pzo2101.cloth_trait in traits:
                hardness = 1
            elif pzo2101.leather_trait in traits:
                hardness = 4
            else:
                hardness = 9
            armor.hardness = hardness
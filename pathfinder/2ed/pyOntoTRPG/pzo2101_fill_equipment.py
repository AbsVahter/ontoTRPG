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
        for index,row in main.iterrows("Shields"):
            Shield(
                name = main.prepare_name(row['name']),
                price = row['price'],
                ac_bonus = row['ac_bonus'],
                speed_penalty = row['speed_penalty'],
                bulk = row['bulk'],
                hardness = row['hardness'],
                comment = row['comment'],
            )


def fill_gear(pzo2101):
    with pzo2101:
        class Gear_and_services(pzo2101.Equipment):
            comment = ("Your character needs all sorts of items both while exploring and in downtime, ranging from "
                       "rations to climbing gear to fancy clothing, depending on the situation.")
        for index, row in main.iterrows("Adventuring_gear"):
            g = Gear_and_services(
                name = main.prepare_name(row['name']),
                price = row['price'],
            )
            if not pd.isna(row['bulk']): g.bulk = row['bulk']
            if not pd.isna(row['hands']): g.hands = row['hands']
            if not pd.isna(row['level']): g.level = row['level']
            if not pd.isna(row['is_uncommon']):
                g.has_trait.append(pzo2101[pzo2101_fill_traits.prepare_trait_name('uncommon')])
            if not pd.isna(row['comment']): g.comment = row['comment']

        for index, row in main.iterrows("Adventuring_gear_corpus"):
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

        for index, row in main.iterrows('Equipment_packs'):
            pack = Equipment_pack(
                name = main.prepare_name(row['name']),
                price = row['price'],
                bulk = row['bulk'],
                comment = row['comment'],
            )
            main.set_relation(pzo2101, pack, contains, row['inside'], func = main.prepare_name)


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
        for index, row in main.iterrows("Traits"):
            if not pd.isna(row['is_weapon_group']) and row['is_weapon_group'] == 1:
                trait = pzo2101[pzo2101_fill_traits.prepare_trait_name(row['name'])]
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

        class Weapon_by_complexity(Weapon):
            pass

        class damage(Weapon >> str, FunctionalProperty): pass
        class range(Weapon >> int, FunctionalProperty): pass
        class reload(Weapon >> int, FunctionalProperty):
            comment = ("While all weapons need some amount of time to get into position, many ranged weapons also need "
                       "to be loaded and reloaded. This entry indicates how many Interact actions it takes to reload "
                       "such weapons.")

        class Weapon_by_group(pzo2101.Weapon): pass

        for index, row in main.iterrows("Weapons"):
            cl = types.new_class(row['class'], (Weapon_by_complexity,))
            w = cl(
                name = main.prepare_name(row['name']),
                damage = row['damage'],
                bulk = row['bulk'],
                hands = row['hands'],
            )
            main.set_relation(pzo2101, w, pzo2101['has_trait'], row['traits'], pzo2101_fill_traits.prepare_trait_name)
            if not pd.isna(row['price']): w.price = row['price']
            if not pd.isna(row['range']): w.range = row['range']
            if not pd.isna(row['reload']): w.reload = row['reload']
            w.is_a.append(Weapon_by_group)
            w.comment.append(row['comment'])

        class Ammunition(Equipment): pass
        class ammunition(Weapon >> Ammunition, FunctionalProperty): pass
        for index, row in main.iterrows("Ammunition"):
            ammo = Ammunition(
                name = main.prepare_name(row['name']),
                price = row['price'],
                bulk = row['bulk'],
                comment = row['comment']
            )
            for w in row['weapon'].split(","):
                pzo2101[w].ammunition = ammo

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

        for index, row in main.iterrows("Armors"):
            cl = pzo2101[row['class']]
            if cl is None:
                cl = types.new_class(row['class'], (Armor,))
            armor = cl(
                name = main.prepare_name(row['name']),
                ac_bonus = row['ac_bonus'],
                check_penalty = row['check_penalty'],
                speed_penalty = row['speed_penalty'],
                bulk = row['bulk'],
                has_trait = [pzo2101[pzo2101_fill_traits.prepare_trait_name(t)] for t in str(row['traits']).split(",")]
                    if not pd.isna(row['traits']) else [],
                comment = row['comment'],
            )
            if not pd.isna(row['price']): armor.price = row['price']
            if not pd.isna(row['dex_cap']): armor.dex_cap = row['dex_cap']
            if not pd.isna(row['str_threshold']): armor.str_threshold = row['str_threshold']
            if not pd.isna(row['level']): armor.level = row['level']
            traits = armor.has_trait
            if pzo2101.cloth_trait in traits:
                hardness = 1
            elif pzo2101.leather_trait in traits:
                hardness = 4
            else:
                hardness = 9
            armor.hardness = hardness
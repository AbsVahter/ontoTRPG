import pandas as pd
from owlready2 import *
import main


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

    fill_armor(pzo2101)
    fill_weapon(pzo2101)


def fill_weapon(pzo2101: Ontology):
    with pzo2101:
        class Weapon(pzo2101.Equipment):
            pass

        class Weapon_by_complexity(Weapon):
            pass

        class Weapon_by_commonness(Weapon):
            pass

        for index, row in main.iterrows("Weapons"):
            cl = pzo2101.search(is_a = Weapon, iri = main.iri_for_search(row['class_1'])).first()
            if cl is None:
                cl = types.new_class(row['class_1'], (Weapon_by_complexity,))
            w = cl(main.prepare_name(row['name']))
            cl_2 = pzo2101.search(is_a = Weapon, iri = main.iri_for_search(row['class_2'])).first()
            if cl_2 is None:
                cl_2 = types.new_class(row['class_2'], (Weapon_by_commonness,))
            w.is_a.append(cl_2)


def fill_armor(pzo2101: Ontology):
    with pzo2101:
        class Armor(pzo2101.Equipment):
            comment = ("Armor increases your character’s defenses, but some medium or heavy armor can hamper movement. "
                       "If you want to increase your character’s defense beyond the protection your armor provides, "
                       "they can use a shield. Armor protects your character only while they’re wearing it.")

        class ac_bonus(Armor >> int, FunctionalProperty):
            comment = "This number is the item bonus you add for the armor when determining Armor Class."

        class dex_cap(Armor >> int, FunctionalProperty):
            comment = ("This number is the maximum amount of your Dexterity modifier that can apply to your AC while "
                       "you are wearing a given suit of armor.")

        class check_penalty(Armor >> int, FunctionalProperty):
            comment = ("While wearing your armor, you take this penalty to Strength- and Dexterity-based skill checks, "
                       "except for those that have the attack trait. If you meet the armor’s Strength threshold, "
                       "you don’t take this penalty.")

        class speed_penalty(Armor >> int, FunctionalProperty):
            comment = ("While wearing a suit of armor, you take the penalty listed in this entry to your Speed, "
                       "as well as to any other movement types you have, such as a climb Speed or swim Speed, "
                       "to a minimum Speed of 5 feet. If you meet the armor’s Strength threshold you reduce the "
                       "penalty by 5 feet.")

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
                has_trait = [pzo2101[main.prepare_name(t)] for t in str(row['traits']).split(",")]
                    if not pd.isna(row['traits']) else [],
                comment = row['comment'],
            )
            if not pd.isna(row['price']): armor.price = row['price']
            if not pd.isna(row['dex_cap']): armor.dex_cap = row['dex_cap']
            if not pd.isna(row['str_threshold']): armor.str_threshold = row['str_threshold']
            traits = armor.has_trait
            if pzo2101.cloth in traits:
                hardness = 1
            elif pzo2101.leather in traits:
                hardness = 4
            else:
                hardness = 9
            armor.hardness = hardness
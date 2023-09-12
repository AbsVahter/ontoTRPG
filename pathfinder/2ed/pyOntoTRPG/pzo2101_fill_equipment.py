from owlready2 import *
import main


def fill(pzo2101: Ontology):
    with pzo2101:
        class Equipment(Thing): pass

        fill_weapon(pzo2101)
        fill_armor(pzo2101)


def fill_weapon(pzo2101: Ontology):
    with pzo2101:
        class Weapon(pzo2101.Equipment, pzo2101.With_proficiency_rank): pass

        class Weapon_by_complexity(Weapon): pass
        class Weapon_by_commonness(Weapon): pass

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
        class Armor(pzo2101.Equipment, pzo2101.With_proficiency_rank): pass

        for index, row in main.iterrows("Armors"):
            cl = pzo2101.search(is_a = Armor, iri = main.iri_for_search(row['class'])).first()
            if cl is None:
                cl = types.new_class(row['class'], (Armor,))
            cl(main.prepare_name(row['name']))
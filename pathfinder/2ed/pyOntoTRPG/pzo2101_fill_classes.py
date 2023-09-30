import pandas as pd
from owlready2 import *
import main


def fill_archetypes(pzo2101):
    with pzo2101:
        Feat = pzo2101.Feat

        class Archetype(Feat):
            comment = ("There are infinite possible character concepts, but you might find that the feats and skill "
                       "choices from a single class aren’t sufficient to fully realize your character. Archetypes "
                       "allow you to expand the scope of your character’s class.")

        for gc in pzo2101.Gameclass.instances():
            Archetype(main.render_text(gc.name, object_class = "Archetype"))

        main.fill_onto_from_xml(pzo2101, "Archetype feats", Feat)


def fill_rel_class_kits(pzo2101):
    with pzo2101:
        for pack in pzo2101.Starter_kit.instances():
            gameclass_name = pack.name.split("_s_")[0]
            gc = pzo2101[gameclass_name]
            pack.relates_to.append(gc)


def fill(pzo2101: Ontology):
    fill_class_props(pzo2101)
    fill_weapon(pzo2101)
    fill_armor(pzo2101)
    fill_feats(pzo2101)
    fill_archetypes(pzo2101)
    fill_rel_class_kits(pzo2101)


def fill_class_props(pzo2101: Ontology):
    with pzo2101:
        Gameclass = pzo2101.Gameclass

        Gameclass.comment.append("Just as your character’s ancestry plays a key role in expressing their identity and "
                                 "worldview, their class indicates the training they have and will improve upon as an "
                                 "adventurer. Choosing your character’s class is perhaps the most important decision you will "
                                 "make for them. Groups of players often create characters whose skills and abilities "
                                 "complement each other mechanically—for example, ensuring your party includes a healer, "
                                 "a combatoriented character, a stealthy character, and someone with command over magic—so you "
                                 "may wish to discuss options with your group before deciding.")

        for k in [pzo2101.perception, pzo2101.fortitude, pzo2101.reflex, pzo2101.will]:
            Gameclass.trained.append(k)

        main.fill_onto_from_xml(pzo2101, "Classes", Gameclass)


def fill_weapon(pzo2101: Ontology):
    with pzo2101:
        fist = pzo2101.fist
        Gameclass = pzo2101.Gameclass
        Gameclass.is_a.append(pzo2101.trained.value(fist))
        trained = pzo2101.trained

        wizard = pzo2101.wizard
        for cl in filter(lambda x: x is not wizard, Gameclass.instances()):
            pzo2101.Simple_weapon.is_a.append(Inverse(trained).value(cl))
        for cl in [pzo2101.barbarian, pzo2101.champion, pzo2101.ranger]:
            pzo2101.Martial_weapon.is_a.append(Inverse(trained).value(cl))
        pzo2101.alchemist.trained.append(pzo2101.alchemical_bomb)

        fighter = pzo2101.fighter
        for weapon_cl in [pzo2101.Simple_weapon, pzo2101.Martial_weapon]:
            weapon_cl.is_experted_by.append(fighter)
        pzo2101.Advanced_weapon.is_a.append(Inverse(trained).value(fighter))
        fighter.experted.append(fist)


def fill_armor(pzo2101: Ontology):
    with pzo2101:
        Gameclass = pzo2101.Gameclass
        for arm in pzo2101.Unarmored_as_armor.instances():
            Gameclass.trained.append(arm)
        arm_dict = {
            pzo2101.Light_armor: [pzo2101.alchemist, pzo2101.barbarian, pzo2101.bard, pzo2101.champion, pzo2101.druid,
                                  pzo2101.fighter, pzo2101.ranger, pzo2101.rogue],
            pzo2101.Medium_armor: [pzo2101.alchemist, pzo2101.barbarian, pzo2101.champion, pzo2101.druid,
                                   pzo2101.fighter, pzo2101.ranger],
            pzo2101.Heavy_armor: [pzo2101.champion, pzo2101.fighter],
        }
        for arm_cl in arm_dict:
            for cl in arm_dict[arm_cl]:
                arm_cl.is_a.append(Inverse(pzo2101.trained).value(cl))


def fill_feats(pzo2101: Ontology):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Class feats", pzo2101.Feat)
        main.fill_onto_from_xml(pzo2101, "Class specialization feats", pzo2101.Class_specialization)


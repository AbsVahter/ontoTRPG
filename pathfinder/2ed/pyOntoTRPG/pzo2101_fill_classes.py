import pandas as pd
from owlready2 import *
import main


def fill(pzo2101: Ontology):
    fill_class_props(pzo2101)
    fill_weapon(pzo2101)
    fill_armor(pzo2101)
    fill_feats(pzo2101)
    fill_specializations(pzo2101)


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

        trained = pzo2101.trained
        for k in [pzo2101.perception, pzo2101.fortitude, pzo2101.reflex, pzo2101.will]:
            Gameclass.trained.append(k)

        for index, row in main.iterrows('Classes'):
            skills = []
            if row['skills'] == row['skills']: skills = row['skills'].split(",")
            cl = Gameclass(
                name = main.prepare_name(row['name']),
                comment = [row['comment_1'], row['comment_2']],
                ability_boost = [pzo2101.search(is_a = pzo2101.Ability_score, iri = main.iri_for_search(x)).first()
                                 for x in row['boost'].split(",")],
                hp = int(row['hp']),
                experted = [pzo2101.search(is_a = pzo2101.Characteristic,
                                            iri = main.iri_for_search(x)).first()
                             for x in row['expert'].split(",")],
                trained = [pzo2101.search(is_a = pzo2101.Skill,
                                            iri = main.iri_for_search(x)).first()
                              for x in skills],
                additional_skills = row['additional_skills'],
            )
            if "," in row['boost']:
                cl.comment.append("your class gives you an ability boost to your choice")

        pzo2101.champion.comment.append("Trained in one skill determined by your choice of deity")
        pzo2101.cleric.comment.extend([
            "Trained in one skill determined by your choice of deity",
            "Trained in the favored weapon of your deity. If your deity’s favored weapon is uncommon, you also gain "
            "access to that weapon."
        ])
        pzo2101.druid.comment.append("Trained in one skill determined by your druidic order")
        pzo2101.fighter.comment.append("Trained in your choice of Acrobatics or Athletics")
        pzo2101.rogue.comment.append("Trained in one or more skills determined by your rogue’s racket")
        pzo2101.sorcerer.comment.append("Trained in one or more skills determined by your bloodline")


def fill_weapon(pzo2101: Ontology):
    with pzo2101:
        fist = pzo2101.fist
        Gameclass = pzo2101.Gameclass
        Gameclass.is_a.append(pzo2101.trained.value(fist))

        wizard = pzo2101.wizard
        for cl in filter(lambda x: x is not wizard, Gameclass.instances()):
            pzo2101.Simple_weapon.is_trained_by.append(cl)
        for cl in [pzo2101.barbarian, pzo2101.champion, pzo2101.ranger]:
            pzo2101.Martial_weapon.is_trained_by.append(cl)
        pzo2101.alchemist.trained.append(pzo2101.alchemical_bomb)

        fighter = pzo2101.fighter
        for weapon_cl in [pzo2101.Simple_weapon, pzo2101.Martial_weapon]:
            weapon_cl.is_experted_by.append(fighter)
        pzo2101.Advanced_weapon.is_trained_by.append(fighter)
        fighter.experted.append(fist)

        w_dict = {
            pzo2101.bard: ['longsword', 'rapier', 'sap', 'shortbow', 'shortsword', 'whip'],
            pzo2101.rogue: ['rapier', 'sap', 'shortbow', 'shortsword'],
            wizard: ['club', 'crossbow', 'dagger', 'heavy_crossbow', 'staff']
        }
        for cl in w_dict:
            for w in w_dict[cl]:
                cl.trained.append(
                    pzo2101.search(is_a = pzo2101.Weapon, iri = main.iri_for_search(w)).first())


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
                arm_cl.is_trained_by.append(cl)


def fill_feats(pzo2101: Ontology):
    with pzo2101:
        for index, row in main.iterrows("Class_feats"):
            cl = pzo2101[row['gameclass']]
            f = pzo2101.Feat(
                name = main.prepare_name(row['name']),
                level = int(row['level']),
            )
            if row['property'] == 'feat_of':
                f.feat_of.append(cl)
            elif row['property'] == 'selectable_feat_of':
                f.selectable_feat_of.append(cl)


def fill_specializations(pzo2101):
    with pzo2101:
        for index, row in main.iterrows("Class_specialization_feats"):
            parent_feat = pzo2101.search(is_a = pzo2101.Feat, iri = main.iri_for_search(row['parent'])).first()
            pzo2101.Class_specialization(
                name = main.prepare_name(row['name']),
                selectable_feat_of = [parent_feat],
            )
import pandas as pd
from owlready2 import *

import main


def fill(pzo2101: Ontology):
    create_hierarchy(pzo2101)
    fill_props(pzo2101)
    fill_feats(pzo2101)

def create_hierarchy(pzo2101: Ontology):
    with pzo2101:
        class Concept(Thing): pass
        class has_feat(Concept >> pzo2101.Feat):
            class_property_type = ["some"]
        class trained(Concept >> pzo2101.With_proficiency_rank): pass
        class is_trained_by(ObjectProperty):
            inverse_property = trained
        class has_selectable_feat(Concept >> pzo2101.Feat):
            class_property_type = ["some"]

        class selectable_feat_of(ObjectProperty):
            inverse_property = has_selectable_feat
            class_property_type = ["some"]

        class Ancestry(Concept):
            comment = ("Your character’s ancestry determines which people they call their own, whether it’s diverse "
                       "and ambitious humans, insular but vivacious elves, traditionalist and family-focused dwarves, "
                       "or any of the other folk who call Golarion home. A character’s ancestry and their experiences "
                       "prior to their life as an adventurer—represented by a background—might be key parts of their "
                       "identity, shape how they see the world, and help them find their place in it.")
            has_feat = pzo2101.common_language
            has_selectable_feat = pzo2101.local_language

        class hp(Concept >> int, FunctionalProperty):
            comment = 'hit points'

        class size(Ancestry >> str, FunctionalProperty): pass

        class speed(Ancestry >> int, FunctionalProperty):
            comment = "speed in feet"

        Ability_score = pzo2101.Ability_score
        class ability_boost(Concept >> Ability_score): pass

        class ability_flaw(Ancestry >> Ability_score): pass

        class feat_of(ObjectProperty):
            inverse_property = has_feat

        class Trait(Thing): pass

        class has_trait(Ancestry >> Trait):
            class_property_type = ["some"]

        tHumanoid = Trait('humanoid_trait')
        Ancestry.has_trait.append(tHumanoid)


def fill_props(pzo2101: Ontology):
    with pzo2101:
        Ancestry = pzo2101.Ancestry
        for index, row in main.iterrows("Ancestries"):
            Ancestry(
                name = row['name'],
                comment = row['comment'],
                hp = row['hp'],
                size = row['size'],
                speed = row['speed'],
                ability_boost = [pzo2101.search(is_a = pzo2101.Ability_score, iri = main.iri_for_search(x)).first()
                                 for x in row['boosts'].split(",")] if not pd.isnull(row['boosts']) else [],
                ability_flaw = [pzo2101.search(is_a = pzo2101.Ability_score, iri = main.iri_for_search(x)).first()
                                 for x in row['flaw'].split(",")] if not pd.isnull(row['flaw']) else [],
                has_feat = [pzo2101.search(is_a = pzo2101.Language, iri = main.iri_for_search(x)).first()
                                 for x in row['lang'].split(",")] if not pd.isnull(row['lang']) else [],
                has_selectable_feat = [pzo2101.search(is_a = pzo2101.Language, iri = main.iri_for_search(x)).first()
                                 for x in row['sel_lang'].split(",")] if not pd.isnull(row['sel_lang']) else [],
            )

        pzo2101.Language_common.selectable_feat_of.append(pzo2101.human)


def fill_feats(pzo2101: Ontology):
    with pzo2101:
        Feat = pzo2101.Feat
        f_dict = {
            'Darkvision': [pzo2101.dwarf, pzo2101.goblin],
            'Clan Dagger': [pzo2101.dwarf,],
            'Low-Light Vision': [pzo2101.elf, pzo2101.gnome],
            'Keen Eyes': [pzo2101.halfling]
        }
        for f in f_dict:
            for anc in f_dict[f]:
                anc.has_feat.append(Feat(main.prepare_name(f)))

        for index, row in main.iterrows("Ancestry_feats"):
            cl = pzo2101.search(is_a = Feat, iri = f"*{row['class']}").first()
            anc = pzo2101.search(is_a = pzo2101.Ancestry, iri = main.iri_for_search(row['ancestry'])).first()
            cl(
                name = main.prepare_name(row['name']),
                level = row['level'],
                selectable_feat_of = [anc],
                prereq = [pzo2101.search(is_a = Feat, iri = main.iri_for_search(x)).first()
                                 for x in row['prereq'].split(",")] if not pd.isnull(row['prereq']) else [],
            )
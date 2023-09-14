import pandas as pd
from owlready2 import *

import main
from pzo2101_hierarchy import create


def fill_animal_companions(pzo2101):
    with pzo2101:
        for index, row in main.iterrows("Animal_companions"):
            anim = pzo2101.Animal_companion(
                name = main.prepare_name(row['name']),
                comment = row['comment'],
                size = main.prepare_name(row['size']),
                hp = row['hp'],
                speed = row['speed']
            )
            if not pd.isna(row['special_speed']): anim.special_speed = row['special_speed']

        for index, row in main.iterrows("Animal_companion_specializations"):
            pzo2101.Animal_companion_specialization(
                name = main.prepare_name(row['name']),
            )


def fill_familiar(pzo2101):
    with pzo2101:
        for index, row in main.iterrows("Familiar_abilities"):
            pzo2101.Familiar_ability(
                name = main.prepare_name(row['name']),
            )

        for index, row in main.iterrows("Master_abilities"):
            pzo2101.Master_ability(
                name = main.prepare_name(row['name']),
            )


def fill(pzo2101: Ontology):
    fill_languages(pzo2101)
    fill_props(pzo2101)
    fill_feats(pzo2101)
    fill_animal_companions(pzo2101)
    fill_familiar(pzo2101)


def fill_props(pzo2101: Ontology):
    with pzo2101:
        Ancestry = pzo2101.Playable_ancestry
        Ancestry.comment.append("Your character’s ancestry determines which people they call their own, whether it’s diverse "
                   "and ambitious humans, insular but vivacious elves, traditionalist and family-focused dwarves, "
                   "or any of the other folk who call Golarion home. A character’s ancestry and their experiences "
                   "prior to their life as an adventurer—represented by a background—might be key parts of their "
                   "identity, shape how they see the world, and help them find their place in it.")
        Ancestry.has_feat.append(pzo2101.common_language)
        Ancestry.has_selectable_feat.append(pzo2101.local_language)

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
        tHumanoid = pzo2101.Trait('humanoid_trait')
        Ancestry.has_trait.append(tHumanoid)


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


def fill_languages(pzo2101: Ontology):
    with pzo2101:
        class Language(pzo2101.Feat):
            comment = ["The people of the Inner Sea region speak dozens of different languages, along with hundreds "
                       "of dialects and regional variations. While a character can generally get by with Taldane, "
                       "also known as Common, knowing another language is vital in some regions. Being able to speak "
                       "these tongues can help you with negotiation, spying on enemies, or just conducting simple "
                       "commerce. Languages also afford you the chance to contextualize your character in the world "
                       "and give meaning to your other character choices."]

        class Language_common(Language): pass

        lst_common = ['Common', 'Draconic', 'Dwarven', 'Elven', 'Gnomish', 'Goblin', 'Halfling', 'Jotun', 'Orcish', 'Sylvan', 'Undercommon', 'Local']
        for lang in lst_common:
            Language_common(lang.lower() + "_language")

        class Language_uncommon(Language): pass

        lst_uncommon = ['Abyssal', 'Akio', 'Aquan', 'Auran', 'Celestial', 'Gnoll', 'Ignan', 'Infernal', 'Necril', 'Shadowtongue', 'Terran']
        for lang in lst_uncommon:
            Language_uncommon(lang.lower() + "_language")

        class Language_secret(Language): pass

        Language_secret('druidic_language')
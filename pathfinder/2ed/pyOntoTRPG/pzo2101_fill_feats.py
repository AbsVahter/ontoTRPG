from owlready2 import *
import main


def fill(pzo2101: Ontology):
    with pzo2101:
        class Feat(Thing): pass

        class Heritage(Feat): pass

        class level(Feat >> int, FunctionalProperty): pass

        fill_languages(pzo2101)
        create_feats(pzo2101)


def fill_languages(pzo2101: Ontology):
    with pzo2101:
        class Language(pzo2101.Feat):
            comment = ["The people of the Inner Sea region speak dozens of different languages, along with hundreds "
                       "of dialects and regional variations. While a character can generally get by with Taldane, "
                       "also known as Common, knowing another language is vital in some regions. Being able to speak "
                       "these tongues can help you with negotiation, spying on enemies, or just conducting simple "
                       "commerce. Languages also afford you the chance to contextualize your character in the world "
                       "and give meaning to your other character choices."]

        pzo2101.Language.comment = ("The people of the Inner Sea region speak dozens of different languages, along with "
                                 "hundreds of dialects and regional variations. While a character can generally get "
                                 "by with Taldane, also known as Common, knowing another language is vital in some "
                                 "regions. Being able to speak these tongues can help you with negotiation, "
                                 "spying on enemies, or just conducting simple commerce. Languages also afford you "
                                 "the chance to contextualize your character in the world and give meaning to your "
                                 "other character choices.")

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


def create_feats(pzo2101: Ontology):
    with pzo2101:
        Feat = pzo2101.Feat
        class prereq(Feat >> Feat): pass

        class Skill_feat(pzo2101.Feat): pass
        for index, row in main.iterrows('Skill_feats'):
            Skill_feat(main.prepare_name(row['name']))
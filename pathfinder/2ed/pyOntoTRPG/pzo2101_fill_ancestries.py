import types

import pandas as pd
from owlready2 import *

import main
import pzo2101_fill_traits
from pzo2101_hierarchy import create


def fill_animal_companions(pzo2101):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, 'Animal companions', pzo2101.Animal_companion)
        main.fill_onto_from_xml(pzo2101, 'Animal companion specializations',
                                pzo2101.Animal_companion_specialization)


def fill_familiar(pzo2101):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Familiar abilities", pzo2101.Familiar_ability)
        main.fill_onto_from_xml(pzo2101, "Master abilities", pzo2101.Master_ability)


def fill_creatures(pzo2101):
    with pzo2101:
        class Creature(pzo2101.Ancestry):
            comment = ("The six humanoid ancestries are far from Golarion’s only inhabitants. Many other creatures "
                       "dwell in the world, some kindly and others cruel, some wild and others organized, "
                       "some anthropomorphic and others completely monstrous. Even creatures that are usually foes of "
                       "civilization, and whom brave adventurers face in battle, can sometimes be reasoned with or "
                       "even befriended. Not all of them are evil, and some are actively helpful to their neighbors. "
                       "And some, of course, simply want to be left alone.")
        main.fill_onto_from_xml(pzo2101,"Creatures", Creature)


def fill(pzo2101: Ontology):
    fill_languages(pzo2101)
    fill_props(pzo2101)
    fill_feats(pzo2101)
    fill_animal_companions(pzo2101)
    fill_familiar(pzo2101)
    fill_creatures(pzo2101)


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
        class ability_flaw(Ancestry >> pzo2101.Ability_score): pass
        main.fill_onto_from_xml(pzo2101, "Ancestries", Ancestry)

        pzo2101.Language_common.selectable_feat_of.append(pzo2101.human)
        tHumanoid = pzo2101.Trait(pzo2101_fill_traits.prepare_trait_name('humanoid'))
        Ancestry.has_trait.append(tHumanoid)


def fill_feats(pzo2101: Ontology):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Ancestry feats", pzo2101.Feat)


def prepare_name_lang(s):
    return f"{main.prepare_name(s)}_language"


def fill_languages(pzo2101: Ontology):
    with pzo2101:
        class Language(pzo2101.Feat):
            comment = ["The people of the Inner Sea region speak dozens of different languages, along with hundreds "
                       "of dialects and regional variations. While a character can generally get by with Taldane, "
                       "also known as Common, knowing another language is vital in some regions. Being able to speak "
                       "these tongues can help you with negotiation, spying on enemies, or just conducting simple "
                       "commerce. Languages also afford you the chance to contextualize your character in the world "
                       "and give meaning to your other character choices."]

        main.fill_onto_from_xml(pzo2101, "Languages", Language)

        pzo2101['Language_regional'].relates_to.append(pzo2101[prepare_name_lang('local')])
        pzo2101[prepare_name_lang('Taldane')].equivalent_to.append(pzo2101[prepare_name_lang('Common')])
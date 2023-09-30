import types

import pandas as pd
from owlready2 import *

import main
import pzo2101_fill_ancestries
import pzo2101_fill_spells


def fill_locations(pzo2101):
    with pzo2101:
        f_name = main.prepare_name
        Setting = pzo2101.Setting

        class Location(Setting):
            pass

        class location(Setting >> Location):
            pass

        main.fill_onto_from_xml(pzo2101, "Locations", Location)


def fill_actors(pzo2101):
    with pzo2101:
        f_name = main.prepare_name
        class Actor(pzo2101.Setting): pass
        class Character(Actor): pass
        main.fill_onto_from_xml(pzo2101, 'Characters', Character)

        class Culture(Actor):
            pass

        class ethnicity_of(Culture >> pzo2101.Ancestry, FunctionalProperty):
            pass

        main.fill_onto_from_xml(pzo2101,"Cultures", Culture)
        '''
        for culture_xml in main.iterate_xml_tree("Cultures"):
            culture = Culture(main.render_text(culture_xml.get('name')))
            main.set_relations(pzo2101, culture, culture_xml)
        '''

def fill_events(pzo2101):
    with pzo2101:
        f_name = main.prepare_name
        class Event(pzo2101.Setting): pass
        class after(Event >> Event): pass
        class during(Event >> Event): pass
        class participant(Event >> pzo2101.Actor): pass

        main.fill_onto_from_xml(pzo2101, "Events", Event)


def fill_factions(pzo2101):
    with pzo2101:
        class Faction(pzo2101.Actor):
            comment = ("While nations and faiths command vast resources and control entire regions, they must still "
                       "compete for the loyalty of their followers. In addition to being swayed by church and state, "
                       "many people are influenced by societal groups known as factions. These groups vary wildly in "
                       "size and purpose— from local thieves’ guilds interested only in filling the pockets and "
                       "bellies of their members, to far-reaching, international commercial conglomerates with their "
                       "own private armies.")
        main.fill_onto_from_xml(pzo2101, "Factions", Faction)


def fill_religions(pzo2101):
    with pzo2101:
        class Religion(pzo2101.Actor):
            comment = ("Selection of a deity is critical for certain classes—like champion and cleric—but most "
                       "characters pay respect to at least one deity to find a focus in life and guide their choices, "
                       "especially in times of hardship or need. Some people instead worship a group of deities "
                       "arranged in a pantheon, follow a nondeific religion like the Green Faith, or adhere to a "
                       "specific philosophy. Note that far more deities, religions, and philosophies exist on any "
                       "world, Golarion included, than those detailed below.")
        class Deity(Religion):
            comment = ("Anyone can worship a deity, but those who do so devoutly should take care to pursue the "
                       "faith’s edicts (behaviors the faith encourages) and avoid its anathemas (actions considered "
                       "blasphemous).")
        Alignment = pzo2101.Alignment
        class follower_alignment(Religion >> Alignment): pass
        class alignment(follower_alignment, FunctionalProperty): pass
        class edicts(Religion >> str, FunctionalProperty): pass
        class anathema(Religion >> str, FunctionalProperty): pass
        class divine_font(Deity >> pzo2101.Spell): pass
        class divine_skill(Deity >> pzo2101.Skill, FunctionalProperty): pass
        class favored_weapon(Deity >> pzo2101.Weapon, FunctionalProperty): pass
        class domain(Deity >> pzo2101.Cleric_domain): pass
        class cleric_spell(Deity >> pzo2101.Spell): pass
        for index, row in main.read_text_for_parse('Deities'):
            corpus = row['corpus']
            x = re.search(r"(.*) \((.*)\) (.*) Edicts (.*) Anathema (.*) Follower Alignments (.*) Devotee Benefits Divine Font (.*) Divine Skill (.*) Favored Weapon (.*) Domains (.*) Cleric Spells (.*)",
                          corpus).groups()
            align = pzo2101.search(is_a = Alignment, abbreviation = x[1]).first()
            aligns = [pzo2101.search(is_a = Alignment, abbreviation = k.strip()).first() for k in x[5].split(',')]
            deity = Deity(
                name = main.prepare_name(x[0]),
                alignment = align,
                comment = x[2],
                edicts = x[3],
                anathema = x[4],
                follower_alignment = aligns,
                divine_font = [pzo2101[pzo2101_fill_spells.prepare_spell_name(k)] for k in x[6].split(" or ")],
                divine_skill = pzo2101[main.prepare_name(x[7])],
                favored_weapon = pzo2101[main.prepare_name(x[8])],
                domain = [pzo2101[prepare_name_domain(k)] for k in x[9].split(",")],
                cleric_spell = [pzo2101[pzo2101_fill_spells.prepare_spell_name(k.split(":")[1])]
                                for k in x[10].split(",")]
            )

        class Faith(Religion):
            comment = "Of course, faith can express itself in more ways than venerating a single deity—or a deity at all."
        main.fill_onto_from_xml(pzo2101, "Faiths", Faith)
        Alignment.is_a.append(Inverse(follower_alignment).value(pzo2101['atheism']))


def prepare_name_domain(s):
    return  f"{main.prepare_name(s)}_domain"


def fill_domains(pzo2101):
    with pzo2101:
        class Cleric_domain(pzo2101.Setting): pass
        Spell = pzo2101.Spell
        class spell(Cleric_domain >> Spell): pass
        main.fill_onto_from_xml(pzo2101, "Domains", Cleric_domain)


def fill(pzo2101):
    with pzo2101:
        class Setting(Thing): pass
    fill_locations(pzo2101)
    fill_actors(pzo2101)
    fill_events(pzo2101)
    fill_factions(pzo2101)
    fill_domains(pzo2101)
    fill_religions(pzo2101)

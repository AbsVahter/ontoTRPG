import types

import pandas as pd
from owlready2 import *

import main
import pzo2101_fill_ancestries


def fill(pzo2101):
    with pzo2101:
        f_name = main.prepare_name
        class Lore(Thing): pass

        class Location(Lore): pass
        class location(Lore >> Location): pass
        for index, row in main.iterrows("Locations"):
            location = Location(
                name = f_name(row['name']),
            )
            main.set_relation(pzo2101, location, location.location, row['is_located_in'], f_name)
            main.set_relation(pzo2101, location, location.comment, row['comment'], is_str = True)
        pzo2101[f_name('Isle of Kortos')].equivalent_to.append(pzo2101[f_name('Starstone Isle')])
        for index, row in main.iterrows("Languages"):
            lang = pzo2101[pzo2101_fill_ancestries.prepare_name_lang(row['name'])]
            main.set_relation(pzo2101, lang, lang.location, row['region'], func = f_name)

        class Actor(Lore): pass
        class Character(Actor): pass
        for index, row in main.iterrows("Characters"):
            character = Character(
                name = f_name(row['name']),
            )
            main.set_relation(pzo2101, character, character.comment, row['comment'], is_str = True)

        class Culture(Actor): pass
        class ethnicity_of(Culture >> pzo2101.Ancestry, FunctionalProperty): pass
        for index, row in main.iterrows("Cultures"):
            culture = Culture(f_name(row['name']))
            main.set_relation(pzo2101, culture, culture.comment, row['comment'], is_str = True)
            main.set_relation(pzo2101, culture, ethnicity_of, row['base'], func = f_name)
            main.set_relation(pzo2101, culture, culture.relates_to, row['lang'],
                              func = pzo2101_fill_ancestries.prepare_name_lang)
            main.set_relation(pzo2101, culture, culture.location, row['location'], func = f_name)

        class Event(Lore): pass
        class after(Event >> Event): pass
        class during(Event >> Event): pass
        class participant(Event >> Character): pass
        for index, row in main.iterrows("Events"):
            event = Event(
                name = f_name(row['name']),
            )
            main.set_relation(pzo2101, event, event.location, row['location'], func = f_name)
            main.set_relation(pzo2101, event, event.after, row['after'], func=f_name)
            main.set_relation(pzo2101, event, event.comment, row['comment'], is_str = True)
            main.set_relation(pzo2101, event, event.participant, row['participants'], func = f_name)
import types

from owlready2 import *

import main


def prepare_school_name(s):
    return  f"{main.prepare_name(s).capitalize()}_school"

def prepare_tradition_name(s):
    return f"{main.prepare_name(s).capitalize()}_tradition"

def fill(pzo2101):
    with pzo2101:
        class Spell(Thing):
            comment = ("With special gestures and utterances, a spellcaster can call forth mystic energies, warp the "
                       "mind, protect themself against danger, or even create something from nothing. Each class has "
                       "its own method of learning, preparing, and casting spells, and every individual spell "
                       "produces a specific effect, so learning new spells gives a spellcaster an increasing array of "
                       "options to accomplish their goals.")

        class Spell_by_magical_tradition(Spell): pass
        class Spell_by_school(Spell): pass

        for index, row in main.iterrows("Spell_categories"):
            name = prepare_school_name(row['name']) if row['category'] == 'school' else prepare_tradition_name(row['name'])
            category = Spell_by_school if row['category'] == 'school' else Spell_by_magical_tradition
            cl = types.new_class(name, (category,))
            cl.comment = row['comment']
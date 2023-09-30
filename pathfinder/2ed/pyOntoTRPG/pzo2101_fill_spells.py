import types

from owlready2 import *

import main


def prepare_school_name(s):
    return  f"{main.prepare_name(s).capitalize()}_school"

def prepare_tradition_name(s):
    return f"{main.prepare_name(s).capitalize()}_tradition"


def prepare_spell_name(s):
    return f"{main.prepare_name(s)}_spell"


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

        for index, row in main.read_text_for_parse("Spell_categories"):
            name = prepare_school_name(row['name']) if row['category'] == 'school' else prepare_tradition_name(row['name'])
            category = Spell_by_school if row['category'] == 'school' else Spell_by_magical_tradition
            cl = types.new_class(name, (category,))
            cl.comment = row['comment']

        for index, row in main.read_text_for_parse("Spells_corpus"):
            for spell_text in filter(lambda x: x != "", row['corpus'].split('.')):
                txt = spell_text.split(':')[0].strip()
                name, school_name = re.search(
                    r'(.*)\((.*)\)', txt).groups()
                name = name.strip()
                if len(name.split(' ')[-1]) == 1:
                    name = ' '.join(name.split(' ')[0:-1])
                if name.split(' ')[-1][-1] == ',':
                    name = ' '.join(name.split(' ')[0:-1])
                school = pzo2101.search(is_a = pzo2101.Spell_by_school, iri = f"*{school_name.capitalize()}*").first()
                comment = spell_text.split(':')[1].strip()
                sp = Spell(
                    name = prepare_spell_name(name),
                    comment = comment,
                    level = row['level'],
                )
                sp.is_a.extend([pzo2101[prepare_tradition_name(row['tradition'])], school])

        class Ritual(Spell):
            comment = ("A ritual is an esoteric and complex spell that anyone can cast. It takes much longer to cast a "
                       "ritual than a normal spell, but rituals can have more powerful effects.")
        main.fill_onto_from_xml(pzo2101, "Rituals", Ritual)
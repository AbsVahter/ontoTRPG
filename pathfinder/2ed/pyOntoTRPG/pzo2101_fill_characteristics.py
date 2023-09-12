from owlready2 import *

import main


def fill(pzo2101: Ontology):

    with pzo2101:
        class Characteristic(Thing): pass

        class Ability_score(Characteristic): pass

        for index, row in main.iterrows('Ability_scores'):
            Ability_score(row['name'], comment = row['comment'])

        class With_proficiency_rank(Thing): pass
        class Skill(Characteristic, With_proficiency_rank): pass

        for index, row in main.iterrows('Skills'):
            Skill(row['name'].lower())

        for ch in ['perception', 'fortitude', 'reflex', 'will']:
            Characteristic(ch)

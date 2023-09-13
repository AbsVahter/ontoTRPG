from owlready2 import *

import main


def fill(pzo2101: Ontology):

    with pzo2101:
        Characteristic = pzo2101.Characteristic

        for index, row in main.iterrows('Ability_scores'):
            pzo2101.Ability_score(row['name'], comment = row['comment'])

        class Skill(Characteristic, pzo2101.With_proficiency_rank): pass

        for index, row in main.iterrows('Skills'):
            Skill(row['name'].lower())

        for ch in ['perception', 'fortitude', 'reflex', 'will']:
            Characteristic(ch)

import pandas as pd
from owlready2 import *

import main


def fill_skills(pzo2101):
    with (pzo2101):
        Characteristic = pzo2101.Characteristic

        class Skill(Characteristic):
            comment = ("While your character’s ability scores represent their raw talent and potential, "
                       "skills represent their training and experience at performing certain tasks. Each skill is "
                       "keyed to one of your character’s ability scores and used for an array of related actions. "
                       "Your character’s expertise in a skill comes from several sources, including their background "
                       "and class.")
        class recall_knowledge_specialization(Skill >> str, FunctionalProperty): pass
        main.fill_onto_from_xml(pzo2101,"Skills", Skill)


def fill_abilities(pzo2101):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Ability scores", pzo2101.Ability_score)

def fill(pzo2101):
    with pzo2101:
        Characteristic = pzo2101.Characteristic
        class Characteristic_with_proficiency(Characteristic): pass
        main.fill_onto_from_xml(pzo2101, 'Characteristics', Characteristic)

    fill_abilities(pzo2101)
    fill_skills(pzo2101)

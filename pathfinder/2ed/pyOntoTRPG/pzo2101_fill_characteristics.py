from owlready2 import *

import main


def fill(pzo2101: Ontology):

    with pzo2101:
        Characteristic = pzo2101.Characteristic
        Ability_score = pzo2101.Ability_score

        for index, row in main.iterrows('Ability_scores'):
            Ability_score(row['name'], comment = row['comment'])

        class Skill(Characteristic, pzo2101.With_proficiency_rank):
            comment = ("While your character’s ability scores represent their raw talent and potential, "
                       "skills represent their training and experience at performing certain tasks. Each skill is "
                       "keyed to one of your character’s ability scores and used for an array of related actions. "
                       "Your character’s expertise in a skill comes from several sources, including their background "
                       "and class.")

        class is_tied_to_ability(Skill >> Ability_score, FunctionalProperty): pass

        for index, row in main.iterrows('Skills'):
            Skill(
                name = main.prepare_name(row['name']),
                is_tied_to_ability = pzo2101[row['key_ability']],
            )

        for ch in ['perception', 'fortitude', 'reflex', 'will']:
            Characteristic(ch)

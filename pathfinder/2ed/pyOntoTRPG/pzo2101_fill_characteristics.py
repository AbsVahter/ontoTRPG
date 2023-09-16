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
        for index, row in main.iterrows('Skills'):
            sk = Skill(
                name = main.prepare_name(row['name']),
                relates_to = [pzo2101[row['key_ability']]],
                comment = row['comment'],
            )
            if not pd.isna(row['recall_knowledge']): sk.recall_knowledge_specialization = row['recall_knowledge']
            acts_untrained = row['untrained_actions'].split(",")
            acts_trained = row['trained_actions'].split(",") if not pd.isna(row['trained_actions']) else []
            acts = acts_untrained + acts_trained
            for act in acts:
                pzo2101.Action(
                    name = main.prepare_name(act),
                    need_training = act in acts_trained,
                    relates_to = [sk],
                )


def fill_abilities(pzo2101):
    with pzo2101:
        for index, row in main.iterrows('Ability_scores'):
            pzo2101.Ability_score(row['name'], comment = row['comment'])


def fill_actions(pzo2101):
    with pzo2101:
        for index, row in main.iterrows("Actions"):
            act = pzo2101.search(is_a = pzo2101.Action, iri = main.iri_for_search(row['name'])).first()
            act.comment.append(row['comment'])
            for trait_name in row['traits'].split(" "):
                trait = pzo2101.Trait(main.prepare_name(trait_name))
                act.has_trait.append(trait)


def fill(pzo2101: Ontology):
    fill_abilities(pzo2101)
    fill_skills(pzo2101)
    fill_actions(pzo2101)
    with pzo2101:
        for ch in ['perception', 'fortitude', 'reflex', 'will']:
            pzo2101.Characteristic(ch)

from owlready2 import *
import main


def fill(pzo2101: Ontology):
    with pzo2101:
        fill_skill_feats(pzo2101)


def fill_skill_feats(pzo2101: Ontology):
    with pzo2101:
        class Skill_feat(pzo2101.Feat): pass
        for index, row in main.iterrows('Skill_feats'):
            Skill_feat(main.prepare_name(row['name']))
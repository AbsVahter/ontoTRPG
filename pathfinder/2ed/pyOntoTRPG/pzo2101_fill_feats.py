import pandas as pd
from owlready2 import *
import main


def fill(pzo2101: Ontology):
    with pzo2101:
        fill_general_feats(pzo2101)


def fill_general_feats(pzo2101: Ontology):
    with pzo2101:
        Feat = pzo2101.Feat
        class General_feat(Feat): pass
        class Skill_feat(General_feat): pass
        for index, row in main.iterrows('General_feats'):
            f_name = main.prepare_name(row['name'])
            f = Skill_feat(f_name) if row['is_skill_feat'] == 1 else General_feat(f_name)
            f.level = row['level']
            if not pd.isna(row['prereq_details']):
                f.prereq_details.append(row['prereq_details'])
            if not pd.isna(row['prereq']):
                for req in row['prereq'].split(","):
                    f.prereq.append(pzo2101[main.prepare_name(req)])
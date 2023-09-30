import pandas as pd
from owlready2 import *
import main


def fill(pzo2101: Ontology):
    with pzo2101:
        fill_general_feats(pzo2101)


def prepare_name_feat(s):
    return  f"{main.prepare_name(s)}"


def fill_general_feats(pzo2101: Ontology):
    with pzo2101:
        Feat = pzo2101.Feat
        class General_feat(Feat): pass
        main.fill_onto_from_xml(pzo2101, "General feats", General_feat)
import pandas as pd
from owlready2 import *
import pzo2101_fill_ancestries
import pzo2101_fill_art
import pzo2101_fill_backgrounds
import pzo2101_fill_characteristics
import pzo2101_fill_classes
import pzo2101_fill_equipment
import pzo2101_fill_feats
import pzo2101_fill_spells
import pzo2101_fill_traits
import pzo2101_hierarchy

if __name__ == '__main__':
    owlready2.JAVA_EXE = r"C:\Program Files\Java\jre-1.8\bin\java.exe"
    onto_path.append(r"D:\Ontologies\Created ontologies\trpgontologies\pathfinder\2ed")
    pzo2101 = get_ontology(
        "https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#")

    pzo2101_hierarchy.create(pzo2101)
    pzo2101_fill_characteristics.fill(pzo2101)
    pzo2101_fill_feats.fill(pzo2101)
    pzo2101_fill_traits.fill(pzo2101)
    pzo2101_fill_ancestries.fill(pzo2101)
    pzo2101_fill_backgrounds.fill(pzo2101)
    pzo2101_fill_equipment.fill(pzo2101)
    pzo2101_fill_classes.fill(pzo2101)
    pzo2101_fill_spells.fill(pzo2101)
    pzo2101_fill_art.fill(pzo2101)

    pzo2101.save()


def prepare_name(s):
    return re.sub('\W+', '_', s.split("@")[0].lower().strip())


def iri_for_search(s):
    return f"*{prepare_name(s)}"


def iterrows(file_name):
    return pd.read_csv(f'resources/{file_name}.txt', sep = '\t').iterrows()


def make_dict(lst, func=None):
    f = func if func is not None else prepare_name
    dict = {}
    for k in filter(lambda x: x is not None, lst):
        comment = None if '@' not in k else k.split('@')[1]
        dict[f(k.split('@')[0])] = comment
    return dict


def set_relation(onto, subj, pred, obj_lst, func=None):
    dict = make_dict(obj_lst, func)
    pred.python_name = "tmp"
    for k in dict:
        obj = onto[k]
        subj.tmp.append(obj)
        if dict[k] is not None:
            onto.relation_value[subj, pred, obj] = [dict[k]]

    pred.python_name = pred.name

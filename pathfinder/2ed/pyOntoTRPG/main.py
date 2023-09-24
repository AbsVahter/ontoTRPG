import pandas as pd
from owlready2 import *

import pzo2101_fill_age_of_lost_omens
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
import visualization

if __name__ == '__main__':
    owlready2.JAVA_EXE = r"C:\Program Files\Java\jre-1.8\bin\java.exe"
    path = r"D:\Ontologies\Created ontologies\trpgontologies\pathfinder\2ed"
    onto_path.append(path)
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
    pzo2101_fill_age_of_lost_omens.fill(pzo2101)
    pzo2101_fill_art.fill(pzo2101)

    visualization.show(pzo2101, path)

    pzo2101.save()


def prepare_name(s):
    return re.sub('\W+', '_', s.split("@")[0].lower().strip())


def iri_for_search(s):
    return f"*{prepare_name(s)}"


def iterrows(file_name):
    return pd.read_csv(f'resources/{file_name}.txt', sep = '\t').iterrows()


def make_dict(obj, func=None, is_str=False):
    dict = {}
    if not pd.isna(obj):
        lst = obj.split(',') if not is_str else [obj]
        for k in lst:
            comment = None if '@' not in k else k.split('@')[1]
            key = k.split('@')[0]
            key = key if func is None else func(key)
            dict[key] = comment
    return dict


def set_relation(onto, subj, pred, obj_str, func=None, is_str=False):
    dict = make_dict(obj_str, func, is_str)
    with onto:
        if isinstance(pred, ObjectPropertyClass):
            pred.python_name = "tmp"
            for k in dict:
                obj = k if is_str else onto[k]
                if isinstance(subj.tmp, IndividualValueList):
                    subj.tmp.append(obj)
                else:
                    subj.tmp = obj
                if dict[k] is not None:
                    onto.relation_value[subj, pred, obj] = [dict[k]]
            pred.python_name = pred.name
        else:
            for k in dict:
                obj = k if is_str else onto[k]
                pred.append(obj)
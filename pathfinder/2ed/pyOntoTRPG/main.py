import pandas as pd
from owlready2 import *
import pzo2101_fill_ancestries
import pzo2101_fill_art
import pzo2101_fill_backgrounds
import pzo2101_fill_characteristics
import pzo2101_fill_classes
import pzo2101_fill_equipment
import pzo2101_fill_feats
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
    pzo2101_fill_art.fill(pzo2101)

    pzo2101.save()
'''
    for k in filter(lambda x: (pzo2101.feat_of in x.get_properties()) and (len(x.feat_of) > 1)
                              and (any(pzo2101.Gameclass in m.is_a for m in x.feat_of)), pzo2101.Feat.instances()):
        print(k.name)
'''

def prepare_name(s):
    return re.sub('\W+', '_', s.lower().strip())


def iri_for_search(s):
    return f"*{prepare_name(s)}"


def iterrows(file_name):
    return pd.read_csv(f'resources/{file_name}.txt', sep = '\t').iterrows()
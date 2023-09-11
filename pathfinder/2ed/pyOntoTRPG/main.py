import pandas as pd
from owlready2 import *
import pzo2101_fill_ancestries
import pzo2101_fill_art
import pzo2101_fill_backgrounds
import pzo2101_fill_characteristics
import pzo2101_fill_classes
import pzo2101_fill_feats

if __name__ == '__main__':
    owlready2.JAVA_EXE = r"C:\Program Files\Java\jre-1.8\bin\java.exe"
    onto_path.append(r"D:\Ontologies\Created ontologies\trpgontologies\pathfinder\2ed")
    pzo2101 = get_ontology(
        "https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#")

    pzo2101_fill_characteristics.fill(pzo2101)
    pzo2101_fill_feats.fill(pzo2101)
    pzo2101_fill_ancestries.fill(pzo2101)
    pzo2101_fill_backgrounds.fill(pzo2101)
    pzo2101_fill_classes.fill(pzo2101)
    pzo2101_fill_art.fill(pzo2101)

    pzo2101.save()


def prepare_name(s):
    return re.sub('\W+', '_', s.lower())


def iri_for_search(s):
    return f"*{prepare_name(s)}"


def iterrows(file_name):
    return pd.read_csv(f'resources/{file_name}.txt', sep = '\t').iterrows()

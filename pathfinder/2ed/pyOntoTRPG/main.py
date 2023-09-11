import owlready2
from owlready2 import *
import pzo2101_fill_ancestries
import pzo2101_fill_art
import pzo2101_fill_characteristics
import pzo2101_fill_feats

if __name__ == '__main__':
    owlready2.JAVA_EXE = r"C:\Program Files\Java\jre-1.8\bin\java.exe"
    onto_path.append(r"D:\Ontologies\Created ontologies\trpgontologies\pathfinder\2ed")
    pzo2101 = get_ontology("https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#")
    pzo2101_fill_characteristics.fill(pzo2101)
    pzo2101_fill_feats.fill(pzo2101)
    pzo2101_fill_ancestries.fill(pzo2101)
    pzo2101_fill_art.fill(pzo2101)
    pzo2101.save()

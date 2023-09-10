from owlready2 import *

import ontoFillAncestries

if __name__ == '__main__':
    onto = get_ontology("https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.rdf#")
    set_log_level(9)
    ontoFillAncestries.fill(onto)
    print("finish")

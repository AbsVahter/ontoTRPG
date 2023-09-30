import pandas as pd

import main


def fill_alignments(pzo2101):
    with pzo2101:
        class Alignment(pzo2101.Trait): pass
        main.fill_onto_from_xml(pzo2101, "Alignments", Alignment)


def fill(pzo2101):
    with pzo2101:
        Trait = pzo2101.Trait

        class Specialization_effect(Trait):
            pass
        main.fill_onto_from_xml(pzo2101, "Traits", Trait)

    fill_alignments(pzo2101)

def prepare_trait_name(s):
    return main.prepare_name(s) + "_trait"

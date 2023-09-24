import pandas as pd

import main


def fill(pzo2101):
    with pzo2101:
        Trait = pzo2101.Trait

        class Specialization_effect(Trait):
            pass

        for index, row in main.iterrows("Traits"):
            cl = Specialization_effect if row['spec_eff'] == 1 else Trait
            trait = cl(
                name = prepare_trait_name(row['name']),
            )
            if not pd.isna(row['comment']): trait.comment = row['comment']


def prepare_trait_name(s):
    return main.prepare_name(s) + "_trait"

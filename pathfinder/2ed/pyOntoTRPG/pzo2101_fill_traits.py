import main


def fill(pzo2101):
    with pzo2101:
        Trait = pzo2101.Trait
        class Specialization_effect(Trait): pass
        for index, row in main.iterrows("Traits"):
            cl = Trait if row['spec_eff'] == 1 else Specialization_effect
            cl(
                name = main.prepare_name(row['name']),
                comment = row['comment'],
            )
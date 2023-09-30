import pandas as pd
from owlready2 import *

import main

def fill(pzo2101: Ontology):
    with pzo2101:
        Art = pzo2101.Art

        for anc in filter(lambda x: x.name != 'human',pzo2101.Playable_ancestry.instances()):
            for i in range(2):
                art_path = f"https://2e.aonprd.com/Images/Ancestries/{anc.name.capitalize()}0{i+1}.png"
                art = Art(f"art_{anc.name}_{i+1}", image = [art_path])
                art.depicts.append(anc)

        for heritage in ['Human', 'HalfElf', 'HalfOrc']:
            art_path = f"https://2e.aonprd.com/Images/Ancestries/{heritage}01.png"
            art = Art(f"art_{heritage.lower()}", image = [art_path])
            art.depicts.append(pzo2101.human)


        class Icon(Art): pass

        for cl in pzo2101.Gameclass.instances():
            Icon(
                name = f"art_{cl.name}_icon",
                image = f"https://2e.aonprd.com/Images/Class/{cl.name.capitalize()}_Icon.png",
                depicts = [cl],
            )

        class Map(Art):
            pass

        main.fill_onto_from_xml(pzo2101, "Art", Art)

        religions = list(pzo2101.Deity.instances()) + list(pzo2101.Faith.instances())
        religions.remove(pzo2101['atheism'])
        for religion in religions:
            n = religion.name.replace('_', '') if religion.name != 'prophecies_of_kalistrade' else "ProphetsOfKalistrade"

            Icon(
                name = prepare_name_icon(religion.name),
                image = f"https://2e.aonprd.com/Images/Deities/{n}.png",
                depicts = [religion],
            )


def prepare_name_icon(s):
    return f"art_{main.prepare_name(s)}_icon"
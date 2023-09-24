import pandas as pd
from owlready2 import *

import main


def prepare_name_map(s):
    return f"map_{main.prepare_name(s)}"


def fill(pzo2101: Ontology):
    with pzo2101:
        Art = pzo2101.Art

        Art("art_ancestries_and_backgrounds", image = "https://i.ibb.co/nLLbFPt/art-ancestries-and-backgrounds.jpg")

        for anc in filter(lambda x: x.name != 'human',pzo2101.Playable_ancestry.instances()):
            for i in range(2):
                art_path = f"https://2e.aonprd.com/Images/Ancestries/{anc.name.capitalize()}0{i+1}.png"
                art = Art(f"art_{anc.name}_{i+1}", image = [art_path])
                art.depicts.append(anc)

        for heritage in ['Human', 'HalfElf', 'HalfOrc']:
            art_path = f"https://2e.aonprd.com/Images/Ancestries/{heritage}01.png"
            art = Art(f"art_{heritage.lower()}", image = [art_path])
            art.depicts.append(pzo2101.human)

        bg_art_links = [
            "https://i.ibb.co/nngtHvh/art-background-1.jpg",
            "https://i.ibb.co/QdtCW6s/art-background-2.jpg",
            "https://i.ibb.co/jWYXRS6/art-background-3.jpg",
        ]
        for i in range(len(bg_art_links)):
            Art(
                f"art_backgrounds_{i+1}",
                image = [bg_art_links[i]],
            )

        Art("art_classes", image = "https://i.ibb.co/XJSVLsn/art-classes.jpg")

        class Icon(Art): pass

        for cl in pzo2101.Gameclass.instances():
            Icon(
                name = f"art_{cl.name}_icon",
                image = f"https://2e.aonprd.com/Images/Class/{cl.name.capitalize()}_Icon.png",
                depicts = [cl],
            )

        for index, row in main.iterrows("Art"):
            Art(
                name = f"art_{row['name']}",
                image = row['link'],
                depicts = [pzo2101[x.strip()] for x in row['target'].split(",")] if not pd.isna(row['target']) else [],
            )

        class Map(Art): pass
        for index, row in main.iterrows("Maps"):
            m = Map(
                name = prepare_name_map(row['name']),
                image = row['link'],
            )
            main.set_relation(pzo2101, m, m.depicts, row['depicts'], main.prepare_name)

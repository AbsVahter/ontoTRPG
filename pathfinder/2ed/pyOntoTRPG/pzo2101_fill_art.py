from owlready2 import *


def fill(pzo2101: Ontology):
    with pzo2101:
        Art = pzo2101.Art

        Art("art_ancestries_and_backgrounds", image = "https://ibb.co/Vqqtsw5")

        for anc in filter(lambda x: x.name != 'human',pzo2101.Ancestry.instances()):
            for i in range(2):
                art_path = f"https://2e.aonprd.com/Images/Ancestries/{anc.name.capitalize()}0{i+1}.png"
                art = Art(f"art_{anc.name}_{i+1}", image = [art_path])
                art.depicts.append(anc)

        for heritage in ['Human', 'HalfElf', 'HalfOrc']:
            art_path = f"https://2e.aonprd.com/Images/Ancestries/{heritage}01.png"
            art = Art(f"art_{heritage.lower()}", image = [art_path])
            art.depicts.append(pzo2101.human)

        bg_art_links = [
            "https://ibb.co/yYf7w1L",
            "https://ibb.co/gVhP0Ds",
            "https://ibb.co/2sr4NTn",
        ]
        for i in range(len(bg_art_links)):
            Art(
                f"art_backgrounds_{i+1}",
                image = [bg_art_links[i]],
            )

        Art("art_classes", image = "https://ibb.co/mz6STqn")

        class Icon(Art): pass

        for cl in pzo2101.Gameclass.instances():
            Icon(
                name = f"art_{cl.name}_icon",
                image = f"https://2e.aonprd.com/Images/Class/{cl.name.capitalize()}_Icon.png",
                depicts = [cl],
            )

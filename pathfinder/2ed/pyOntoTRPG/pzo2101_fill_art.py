from owlready2 import *


def fill(pzo2101: Ontology):
    with pzo2101:

        class Art(Thing): pass

        class image(AnnotationProperty):
            namespace = pzo2101.get_namespace("http://schema.org/")

        class depicts(Art >> Thing): pass

        class is_depicted_by(ObjectProperty):
            inverse_property = depicts

        for anc in filter(lambda x: x.name != 'human',pzo2101.Ancestry.instances()):
            for i in range(2):
                art_path = f"https://2e.aonprd.com/Images/Ancestries/{anc.name.capitalize()}0{i+1}.png"
                art = Art(f"art_{anc.name}_{i+1}", image = [art_path])
                art.depicts.append(anc)

        for heritage in ['Human', 'HalfElf', 'HalfOrc']:
            art_path = f"https://2e.aonprd.com/Images/Ancestries/{heritage}01.png"
            art = Art(f"art_{heritage.lower()}", image = [art_path])
            art.depicts.append(pzo2101.human)

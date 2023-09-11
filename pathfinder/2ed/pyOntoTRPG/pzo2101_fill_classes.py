from owlready2 import *


def fill(pzo2101: Ontology):
    with pzo2101:
        class Gameclass(pzo2101.Concept):
            comment = ["Just as your character’s ancestry plays a key role in expressing their identity and "
                       "worldview, their class indicates the training they have and will improve upon as an "
                       "adventurer. Choosing your character’s class is perhaps the most important decision you will "
                       "make for them. Groups of players often create characters whose skills and abilities "
                       "complement each other mechanically—for example, ensuring your party includes a healer, "
                       "a combatoriented character, a stealthy character, and someone with command over magic—so you "
                       "may wish to discuss options with your group before deciding."]
        
from owlready2 import *


def fill(pzo2101: Ontology):
    with pzo2101:
        class Ability_score(Thing):pass
        abils = {
            'strength': "Strength measures your character’s physical power. Strength is important if your character "
                        "plans to engage in hand-to-hand combat. Your Strength modififier gets added to melee damage "
                        "rolls and determines how much your character can carry.",
            'dexterity': "Dexterity measures your character’s agility, balance, and reflflexes. Dexterity is important "
                         "if your character plans to make attacks with ranged weapons or use stealth to surprise foes. "
                         "Your Dexterity modififier is also added to your character’s AC and Reflflex saving throws.",
            'constitution': "Constitution measures your character’s overall health and stamina. Constitution is an "
                            "important statistic for all characters, especially those who fifight in close combat. Your "
                            "Constitution modififier is added to your Hit Points and Fortitude saving throws.",
            'intelligence': "Intelligence measures how well your character can learn and reason. A high Intelligence "
                            "allows your character to analyze situations and understand patterns, and it means they can "
                            "become trained in additional skills and might be able to master additional languages.",
            'wisdom': "Wisdom measures your character’s common sense, awareness, and intuition. Your Wisdom modififier "
                      "is added to your Perception and Will saving throws.",
            'charisma': "Charisma measures your character’s personal magnetism and strength of personality. A high "
                          "Charisma score helps you inflfluence the thoughts and moods of others."}
        for abil in abils:
            Ability_score(abil, comment = abils[abil])

from owlready2 import *


def create(pzo2101: Ontology):
    with pzo2101:
        class relation_value(AnnotationProperty): pass
        class relates_to(Thing >> Thing, SymmetricProperty): pass
        class Feat(Thing):
            comment = ("All kinds of experiences and training can shape your character beyond what you learn by "
                       "advancing in your class. Abilities that require a degree of training but can be learned by "
                       "anyone—not only members of certain ancestries or classes—are called general feats.")

        class has_feat(Feat >> Feat): class_property_type = ["some"]

        class feat_of(ObjectProperty): inverse_property = has_feat

        class trained(Feat >> Thing): pass

        class has_selectable_feat(has_feat): pass

        class selectable_feat_of(ObjectProperty): inverse_property = has_selectable_feat

        class Character_backbone_feat(Feat): pass

        class Ancestry(Character_backbone_feat): pass

        class Playable_ancestry(Ancestry): pass

        class Animal_companion(Ancestry): comment = "An animal companion is a loyal comrade who follows your orders."

        class hp(Character_backbone_feat >> int, FunctionalProperty): comment = 'hit points'

        class size(Ancestry >> str, FunctionalProperty): pass

        class speed(Ancestry >> int, FunctionalProperty): comment = "land speed in feet"

        class special_speed(Ancestry >> str, FunctionalProperty): comment = "speed different from land speed"

        class Characteristic(Thing): pass
        class Ability_score(pzo2101.Characteristic): pass
        class ability_boost(Character_backbone_feat >> Ability_score): pass

        class Trait(Thing): pass

        class has_trait(Thing >> Trait): class_property_type = ["some"]

        class level(Thing >> int, FunctionalProperty): pass

        class Heritage(Feat): pass

        class prereq(Thing >> Thing): pass
        class prereq_details(Thing >> str): pass

        class Gameclass(Character_backbone_feat): pass

        class additional_skills(Gameclass >> int, FunctionalProperty): pass

        class experted(trained): pass

        class is_experted_by(ObjectProperty): inverse_property = experted

        class Class_specialization(Feat): pass

        class Background(Character_backbone_feat): pass

        class lore_speciality(Background >> str, FunctionalProperty): pass

        class Art(Thing): pass

        class image(AnnotationProperty): namespace = pzo2101.get_namespace("http://schema.org/")

        class depicts(Art >> Thing): pass

        class is_depicted_by(ObjectProperty): inverse_property = depicts

        class Spellcaster_class(Gameclass): pass

        class spells_per_day(Spellcaster_class >> int, FunctionalProperty):
            comment = ("Base count of spells per day, X.\n"
                       "Spells per day: cantrips = 5,  count of n-level spells = {level <= (n-1)*2: 0; level = (2*n - "
                       "1): X - 1; level >= 2*n: X}.")

        class Animal_companion_specialization(Feat):
            comment = "Specialized animal companions are more intelligent and engage in more complex behaviors."

        class Familiar_ability(Feat): pass

        class Master_ability(Feat): pass

        class abbreviation(AnnotationProperty): pass
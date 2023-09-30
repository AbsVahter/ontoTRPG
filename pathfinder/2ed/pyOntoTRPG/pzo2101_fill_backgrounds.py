from owlready2 import *
import main
import re


def fill(pzo2101: Ontology):
    with pzo2101:
        Background = pzo2101.Background
        Background.comment.append(
           "Backgrounds allow you to customize your character based on their life before adventuring. This "
           "is the next step in their life story after their ancestry, which reflects the circumstances "
           "of their birth. Your character’s background can help you learn or portray more about their "
           "personality while also suggesting what sorts of things they’re likely to know. Consider what "
           "events set your character on their path to the life of an adventurer and how those "
           "circumstances relate to their background.")

        Background.trained.append(pzo2101.lore)

        for index, row in main.read_text_for_parse('Backgrounds'):
            x = re.search(
                r'(.*) BACKGROUND (.*) Choose two ability boosts. One must be to (.*) or (.*), and one is a free ability boost. You’re trained in the (.*) skill and (.*). You gain the (.*) skill feat.',
                row['description']).groups()
            Background(
                main.prepare_name(x[0]),
                comment = x[1],
                ability_boost = [
                    pzo2101.search(is_a = pzo2101.Ability_score, iri = main.iri_for_search(x[2])).first(),
                    pzo2101.search(is_a = pzo2101.Ability_score, iri = main.iri_for_search(x[3])).first(),
                ],
                trained = pzo2101.search(is_a = pzo2101.Skill, iri = main.iri_for_search(x[4])),
                lore_speciality = x[5],
                has_feat = pzo2101.search(is_a = pzo2101.Skill_feat, iri = main.iri_for_search(x[6])),
            )

        # exceptions in background's descriptions
        pzo2101.hermit.trained.append(pzo2101.occultism)
        pzo2101.hermit.comment.append("You’re trained in the Nature or Occultism skill")
        pzo2101.martial_disciple.trained.append(pzo2101.athletics)
        pzo2101.martial_disciple.has_feat.append(pzo2101.quick_jump)
        pzo2101.martial_disciple.comment.append("You’re trained in your choice of the Acrobatics or Athletics skill. "
                                                "You gain a skill feat: Cat Fall if you chose Acrobatics or Quick "
                                                "Jump if you chose Athletics.")
        pzo2101.scholar.trained.extend([pzo2101.nature, pzo2101.occultism, pzo2101.religion])
        pzo2101.scholar.comment.append("You’re trained in your choice of the Arcana, Nature, Occultism, or Religion "
                                       "skill, and gain the Assurance skill feat in your chosen skill.")

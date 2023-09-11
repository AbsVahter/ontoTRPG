from owlready2 import *


def fill(pzo2101: Ontology):
    with pzo2101:
        class Concept(Thing): pass

        class Ancestry(Concept):
            comment = ("Your character’s ancestry determines which people they call their own, whether it’s diverse "
                       "and ambitious humans, insular but vivacious elves, traditionalist and family-focused dwarves, "
                       "or any of the other folk who call Golarion home. A character’s ancestry and their experiences "
                       "prior to their life as an adventurer—represented by a background—might be key parts of their "
                       "identity, shape how they see the world, and help them find their place in it.")

        class hp(Ancestry >> int, FunctionalProperty): pass

        pzo2101.hp.comment = 'hit points'

        class size(Ancestry >> str, FunctionalProperty): pass

        class speed(Ancestry >> int, FunctionalProperty):
            comment = "speed in feet"

        class ability_boost(Concept >> pzo2101.Ability_score): pass

        class ability_flaw(Ancestry >> pzo2101.Ability_score): pass

        class has_feat(Concept >> pzo2101.Feat): pass

        class has_selectable_feat(Ancestry >> pzo2101.Feat): pass

        Ancestry.is_a.extend([has_feat.value(pzo2101.common_language) & has_selectable_feat.value(pzo2101.local_language)])

        ancs = {
            'dwarf': {
                'comment': "Dwarves have a well-earned reputation as a stoic and stern people, ensconced within "
                           "citadels and cities carved from solid rock. While some see them as dour and humorless "
                           "crafters of stone and metal, dwarves and those who have spent time among them understand "
                           "their unbridled zeal for their work, caring far more about quality than quantity. To a "
                           "stranger, they can seem untrusting and clannish, but to their friends and family, "
                           "they are warm and caring, their halls filled with the sounds of laughter and hammers "
                           "hitting anvils.",
                'hp': 10,
                'size': 'medium',
                'speed': 20,
                'boosts': [pzo2101.constitution, pzo2101.wisdom],
                'flaw': [pzo2101.charisma],
                'lang': [pzo2101.dwarven_language],
                'sel_lang': [pzo2101.gnomish_language, pzo2101.goblin_language, pzo2101.jotun_language,
                             pzo2101.orcish_language,
                             pzo2101.terran_language, pzo2101.undercommon_language],
                'feats': [pzo2101.darkvision, pzo2101.clan_dagger],
                'sel_feats': [pzo2101.dwarven_lore, pzo2101.dwarven_weapon_familiarity, pzo2101.rock_runner,
                              pzo2101.stonecunning, pzo2101.unburdened_iron, pzo2101.vengeful_hatred,
                              pzo2101.boulder_roll, pzo2101.dwarven_weapon_cunning, pzo2101.mountain_s_stoutness,
                              pzo2101.stonewalker, pzo2101.dwarven_weapon_expertise],
            },
            'elf': {
                'comment': "As an ancient people, elves have seen great change and have the perspective that can come "
                           "only from watching the arc of history. After leaving the world in ancient times, "
                           "they returned to a changed land, and they still struggle to reclaim their ancestral homes, "
                           "most notably from terrible demons that have invaded parts of their lands. To some, "
                           "the elves are objects of awe—graceful and beautiful, with immense talent and knowledge. "
                           "Among themselves, however, the elves place far more importance on personal freedom than on "
                           "living up to these ideals.",
                'hp': 6,
                'size': 'medium',
                'speed': 30,
                'boosts': [pzo2101.dexterity, pzo2101.intelligence],
                'flaw': [pzo2101.constitution],
                'lang': [pzo2101.elven_language],
                'sel_lang': [pzo2101.celestial_language, pzo2101.draconic_language, pzo2101.gnoll_language,
                             pzo2101.gnomish_language, pzo2101.goblin_language, pzo2101.orcish_language,
                             pzo2101.sylvan_language],
                'feats': [pzo2101.low_light_vision],
                'sel_feats': [pzo2101.ancestral_longevity, pzo2101.elven_lore, pzo2101.elven_weapon_familiarity,
                              pzo2101.forlorn, pzo2101.nimble_elf, pzo2101.otherworldly_magic, pzo2101.unwavering_mien,
                              pzo2101.ageless_patience, pzo2101.elven_weapon_elegance, pzo2101.elf_step,
                              pzo2101.expert_longevity, pzo2101.universal_longevity, pzo2101.elven_weapon_expertise],
            },
            'gnome': {
                'comment': "Long ago, early gnome ancestors emigrated from the First World, realm of the fey. While "
                           "it’s unclear why the first gnomes wandered to Golarion, this lineage manifests in modern "
                           "gnomes as bizarre reasoning, eccentricity, obsessive tendencies, and what some see as "
                           "naivete. These qualities are further reflected in their physical characteristics, "
                           "such as spindly limbs, brightly colored hair, and childlike and extremely expressive facial "
                           "features that further reflect their otherworldly origins.",
                'hp': 8,
                'size': 'small',
                'speed': 25,
                'boosts': [pzo2101.constitution, pzo2101.charisma],
                'flaw': [pzo2101.strength],
                'lang': [pzo2101.gnomish_language, pzo2101.sylvan_language],
                'sel_lang': [pzo2101.draconic_language, pzo2101.dwarven_language, pzo2101.elven_language,
                             pzo2101.goblin_language, pzo2101.jotun_language, pzo2101.orcish_language],
                'feats': [pzo2101.low_light_vision],
                'sel_feats': [pzo2101.animal_accomplice, pzo2101.burrow_elocutionist, pzo2101.fey_fellowship,
                              pzo2101.first_world_magic, pzo2101.gnome_obsession, pzo2101.gnome_weapon_familiarity,
                              pzo2101.illusion_sense, pzo2101.animal_elocutionist, pzo2101.energized_font,
                              pzo2101.gnome_weapon_innovator, pzo2101.first_world_adept, pzo2101.vivacious_conduit,
                              pzo2101.gnome_weapon_expertise],
            },
            'goblin': {
                'comment': "The convoluted histories other people cling to don’t interest goblins. These small folk "
                           "live in the moment, and they prefer tall tales over factual records. The wars of a few "
                           "decades ago might as well be from the ancient past. Misunderstood by other people, "
                           "goblins are happy how they are. Goblin virtues are about being present, creative, "
                           "and honest. They strive to lead fulfilled lives, rather than worrying about how their "
                           "journeys will end. To tell stories, not nitpick the facts. To be small, but dream big.",
                'hp': 6,
                'size': 'small',
                'speed': 25,
                'boosts': [pzo2101.dexterity, pzo2101.charisma],
                'flaw': [pzo2101.wisdom],
                'lang': [pzo2101.goblin_language],
                'sel_lang': [pzo2101.draconic_language, pzo2101.dwarven_language, pzo2101.gnoll_language,
                             pzo2101.gnomish_language, pzo2101.halfling_language, pzo2101.orcish_language],
                'feats': [pzo2101.darkvision],
                'sel_feats': [pzo2101.burn_it_, pzo2101.city_scavenger, pzo2101.goblin_lore, pzo2101.goblin_scuttle,
                              pzo2101.goblin_song, pzo2101.goblin_weapon_familiarity, pzo2101.junk_tinker,
                              pzo2101.rough_rider, pzo2101.very_sneaky, pzo2101.goblin_weapon_frenzy,
                              pzo2101.cave_climber, pzo2101.skittering_scuttle, pzo2101.goblin_weapon_expertise,
                              pzo2101.very_very_sneaky],
            },
            'halfling': {
                'comment': "Claiming no place as their own, halflings control few settlements larger than villages. "
                           "Instead, they frequently live among humans within the walls of larger cities, carving out "
                           "small communities alongside taller folk. Many halflings lead perfectly fulfilling lives in "
                           "the shadows of their larger neighbors, while others prefer a nomadic existence, "
                           "traveling the world and taking advantage of opportunities and adventures as they come.",
                'hp': 6,
                'size': 'small',
                'speed': 25,
                'boosts': [pzo2101.dexterity, pzo2101.wisdom],
                'flaw': [pzo2101.strength],
                'lang': [pzo2101.halfling_language],
                'sel_lang': [pzo2101.dwarven_language, pzo2101.elven_language, pzo2101.gnomish_language,
                             pzo2101.goblin_language],
                'feats': [pzo2101.keen_eyes],
                'sel_feats': [pzo2101.distracting_shadows, pzo2101.halfling_lore, pzo2101.halfling_luck,
                              pzo2101.halfling_weapon_familiarity, pzo2101.sure_feet, pzo2101.titan_slinger,
                              pzo2101.unfettered_halfling, pzo2101.watchful_halfling, pzo2101.cultural_adaptability,
                              pzo2101.halfling_weapon_trickster, pzo2101.guiding_luck, pzo2101.irrepressible,
                              pzo2101.ceaseless_shadows, pzo2101.halfling_weapon_expertise],
            },
            'human': {
                'comment': "As unpredictable and varied as any of Golarion’s peoples, humans have exceptional drive and "
                           "the capacity to endure and expand. Though many civilizations thrived before humanity rose "
                           "to prominence, humans have built some of the greatest and the most terrible societies "
                           "throughout the course of history, and today they are the most populous people in the realms "
                           "around the Inner Sea.",
                'hp': 8,
                'size': 'medium',
                'speed': 25,
                'boosts': [],
                'flaw': [],
                'lang': [],
                'sel_lang': [],
                'feats': [],
                'sel_feats': [pzo2101.adapted_cantrip, pzo2101.cooperative_nature, pzo2101.general_training,
                              pzo2101.haughty_obstinacy, pzo2101.natural_ambition, pzo2101.natural_skill,
                              pzo2101.unconventional_weaponry, pzo2101.elf_atavism, pzo2101.monstrous_peacemaker,
                              pzo2101.orc_ferocity, pzo2101.orc_sight, pzo2101.orc_superstition,
                              pzo2101.orc_weapon_familiarity, pzo2101.adaptive_adept,
                              pzo2101.clever_improviser, pzo2101.inspire_imitation, pzo2101.supernatural_charm,
                              pzo2101.orc_weapon_carnage, pzo2101.victorious_vigor, pzo2101.cooperative_soul,
                              pzo2101.incredible_improvisation, pzo2101.multitalented, pzo2101.pervasive_superstition,
                              pzo2101.unconventional_expertise, pzo2101.incredible_ferocity,
                              pzo2101.orc_weapon_expertise],
            }
        }

        for anc_name in ancs:
            props = ancs[anc_name]
            Ancestry(
                anc_name,
                comment = props['comment'],
                hp = props['hp'],
                size = props['size'],
                speed = props['speed'],
                ability_boost = props['boosts'],
                ability_flaw = props['flaw'],
                has_feat = props['lang'] + props['feats'],
                has_selectable_feat = props['sel_lang'] +
                                      list(filter(lambda x: 'half_' not in x.iri,
                                                  pzo2101.search(type = pzo2101.Heritage,
                                                                 iri = '*' + anc_name + '*'))) +
                                      props['sel_feats'],
            )

        class selectable_feat_of(ObjectProperty):
            inverse_property = has_selectable_feat

        class feat_of(ObjectProperty):
            inverse_property = has_feat

        pzo2101.Language_common.is_a.append(selectable_feat_of.value(pzo2101.human))

        class Trait(Thing): pass

        class has_trait(Ancestry >> Trait): pass

        tHumanoid = Trait('humanoid_trait')
        Ancestry.is_a.append(has_trait.value(tHumanoid))

        pzo2101.human.has_selectable_feat.extend(
            list(filter(lambda x: x.selectable_feat_of == [], pzo2101.Heritage.instances())))

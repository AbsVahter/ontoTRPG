from owlready2 import *
import main


def fill(pzo2101: Ontology):
    with pzo2101:
        class Feat(Thing): pass

        class Heritage(Feat): pass

        class level(Feat >> int, FunctionalProperty): pass

        fill_languages(pzo2101)
        create_feats(pzo2101)


def fill_languages(pzo2101: Ontology):
    with pzo2101:
        class Language(pzo2101.Feat):
            comment = ["The people of the Inner Sea region speak dozens of different languages, along with hundreds "
                       "of dialects and regional variations. While a character can generally get by with Taldane, "
                       "also known as Common, knowing another language is vital in some regions. Being able to speak "
                       "these tongues can help you with negotiation, spying on enemies, or just conducting simple "
                       "commerce. Languages also afford you the chance to contextualize your character in the world "
                       "and give meaning to your other character choices."]

        pzo2101.Language.comment = ("The people of the Inner Sea region speak dozens of different languages, along with "
                                 "hundreds of dialects and regional variations. While a character can generally get "
                                 "by with Taldane, also known as Common, knowing another language is vital in some "
                                 "regions. Being able to speak these tongues can help you with negotiation, "
                                 "spying on enemies, or just conducting simple commerce. Languages also afford you "
                                 "the chance to contextualize your character in the world and give meaning to your "
                                 "other character choices.")

        class Language_common(Language): pass

        lst_common = ['Common', 'Draconic', 'Dwarven', 'Elven', 'Gnomish', 'Goblin', 'Halfling', 'Jotun', 'Orcish', 'Sylvan', 'Undercommon', 'Local']
        for lang in lst_common:
            Language_common(lang.lower() + "_language")

        class Language_uncommon(Language): pass

        lst_uncommon = ['Abyssal', 'Akio', 'Aquan', 'Auran', 'Celestial', 'Gnoll', 'Ignan', 'Infernal', 'Necril', 'Shadowtongue', 'Terran']
        for lang in lst_uncommon:
            Language_uncommon(lang.lower() + "_language")

        class Language_secret(Language): pass

        Language_secret('druidic_language')


def create_feats(pzo2101: Ontology):
    with pzo2101:
        feats_anc = ['Darkvision', 'Clan Dagger', 'Low-Light Vision', 'Keen Eyes']
        for f in feats_anc:
            pzo2101.Feat(main.prepare_name(f))

        feats_heritage = [
            'Ancient-Blooded Dwarf', 'Death Warden Dwarf', 'Forge Dwarf', 'Rock Dwarf', 'Strong-Blooded Dwarf',
            'Arctic Elf', 'Cavern Elf', 'Seer Elf', 'Whisper Elf', 'Woodland Elf',
            'Chameleon Gnome', 'Fey-touched Gnome', 'Sensate Gnome', 'Umbral Gnome', 'Wellspring Gnome',
            'Charhide Goblin', 'Irongut Goblin', 'Razortooth Goblin', 'Snow Goblin', 'Unbreakable Goblin',
            'Gutsy Halfling', 'Hillock Halfling', 'Nomadic Halfling', 'Twilight Halfling', 'Wildwood Halfling',
            'Half-Elf', 'Half-Orc', 'Skilled Heritage', 'Versatile Heritage'
        ]
        for f in feats_heritage:
            pzo2101.Heritage(main.prepare_name(f))

        feats_anc_sel = {
            1: ['DWARVEN LORE', 'DWARVEN WEAPON FAMILIARITY', 'ROCK RUNNER', 'STONECUNNING', 'UNBURDENED IRON',
                'VENGEFUL HATRED', 'ANCESTRAL LONGEVITY', 'ELVEN LORE', 'ELVEN WEAPON FAMILIARITY', 'FORLORN',
                'NIMBLE ELF', 'OTHERWORLDLY MAGIC', 'UNWAVERING MIEN', 'ANIMAL ACCOMPLICE', 'BURROW ELOCUTIONIST',
                'FEY FELLOWSHIP', 'FIRST WORLD MAGIC', 'GNOME OBSESSION', 'GNOME WEAPON FAMILIARITY', 'ILLUSION SENSE',
                'BURN IT!', 'CITY SCAVENGER', 'GOBLIN LORE', 'GOBLIN SCUTTLE', 'GOBLIN SONG',
                'GOBLIN WEAPON FAMILIARITY', 'JUNK TINKER', 'ROUGH RIDER', 'VERY SNEAKY', 'DISTRACTING SHADOWS',
                'HALFLING LORE', 'HALFLING LUCK', 'HALFLING WEAPON FAMILIARITY', 'SURE FEET', 'TITAN SLINGER',
                'UNFETTERED HALFLING', 'WATCHFUL HALFLING', 'ADAPTED CANTRIP', 'COOPERATIVE NATURE', 'GENERAL TRAINING',
                'HAUGHTY OBSTINACY', 'NATURAL AMBITION', 'NATURAL SKILL', 'UNCONVENTIONAL WEAPONRY', 'ELF ATAVISM',
                'MONSTROUS PEACEMAKER', 'ORC FEROCITY', 'ORC SIGHT', 'ORC SUPERSTITION', 'ORC WEAPON FAMILIARITY'],
            5: ['BOULDER ROLL', 'DWARVEN WEAPON CUNNING', 'AGELESS PATIENCE', 'ELVEN WEAPON ELEGANCE',
                'ANIMAL ELOCUTIONIST', 'ENERGIZED FONT', 'GNOME WEAPON INNOVATOR', 'GOBLIN WEAPON FRENZY',
                'CULTURAL ADAPTABILITY', 'HALFLING WEAPON TRICKSTER', 'ADAPTIVE ADEPT', 'CLEVER IMPROVISER',
                'INSPIRE IMITATION', 'SUPERNATURAL CHARM', 'ORC WEAPON CARNAGE', 'VICTORIOUS VIGOR'],
            9: ['MOUNTAIN’S STOUTNESS', 'STONEWALKER', 'ELF STEP', 'EXPERT LONGEVITY', 'FIRST WORLD ADEPT',
                'VIVACIOUS CONDUIT', 'CAVE CLIMBER', 'SKITTERING SCUTTLE', 'GUIDING LUCK', 'IRREPRESSIBLE',
                'COOPERATIVE SOUL', 'INCREDIBLE IMPROVISATION', 'MULTITALENTED', 'PERVASIVE SUPERSTITION'],
            13: ['DWARVEN WEAPON EXPERTISE', 'UNIVERSAL LONGEVITY', 'ELVEN WEAPON EXPERTISE', 'GNOME WEAPON EXPERTISE',
                 'GOBLIN WEAPON EXPERTISE', 'VERY, VERY SNEAKY', 'CEASELESS SHADOWS', 'HALFLING WEAPON EXPERTISE',
                 'UNCONVENTIONAL EXPERTISE', 'INCREDIBLE FEROCITY', 'ORC WEAPON EXPERTISE'],
        }
        for lvl in feats_anc_sel:
            lst = feats_anc_sel[lvl]
            for f in lst:
                pzo2101.Feat(main.prepare_name(f), level = lvl)

        class prereq(pzo2101.Feat >> pzo2101.Heritage): pass

        for f in [pzo2101.elf_atavism, pzo2101.inspire_imitation, pzo2101.supernatural_charm]:
            f.prereq.append(pzo2101.half_elf)
        for f in [pzo2101.monstrous_peacemaker, pzo2101.orc_ferocity, pzo2101.orc_sight, pzo2101.orc_superstition,
            pzo2101.orc_weapon_familiarity, pzo2101.orc_weapon_carnage, pzo2101.victorious_vigor,
            pzo2101.pervasive_superstition, pzo2101.incredible_ferocity, pzo2101.orc_weapon_expertise]:
            f.prereq.append(pzo2101.half_orc)

        class Skill_feat(pzo2101.Feat): pass
        for index, row in main.iterrows('Skill_feats'):
            Skill_feat(main.prepare_name(row['name']))

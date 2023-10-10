from email.errors import CharsetError

from owlready2 import *
import main


def create_hierarchy(pzo2101):
    with pzo2101:
        class relation_value(AnnotationProperty):
            pass

        class relation_argument(AnnotationProperty):
            pass

        class relation_prereq(AnnotationProperty):
            pass

        class relation_order(AnnotationProperty):
            pass

        class selects(Thing >> Thing):
            pass

        class relates_to(Thing >> Thing, SymmetricProperty):
            pass

        class Gamerule(Thing):
            pass

        class Feat(Thing):
            comment = ("All kinds of experiences and training can shape your character beyond what you learn by "
                       "advancing in your class. Abilities that require a degree of training but can be learned by "
                       "anyone—not only members of certain ancestries or classes—are called general feats.")

        class has_feat(Feat >> Feat):
            pass

        class feat_of(ObjectProperty):
            inverse_property = has_feat

        class trained(Feat >> Thing):
            pass

        class has_selectable_feat(has_feat):
            pass

        class selectable_feat_of(ObjectProperty):
            inverse_property = has_selectable_feat

        class Character_backbone_feat(Feat):
            pass

        class Ancestry(Character_backbone_feat):
            pass

        class Playable_ancestry(Ancestry):
            pass

        class Animal_companion(Ancestry):
            comment = "An animal companion is a loyal comrade who follows your orders."

        class hp(Character_backbone_feat >> int, FunctionalProperty):
            comment = 'hit points'

        class size(Ancestry >> str, FunctionalProperty):
            pass

        class speed(Ancestry >> int, FunctionalProperty):
            comment = "land speed in feet"

        class special_speed(Ancestry >> str, FunctionalProperty):
            comment = "speed different from land speed"

        class Characteristic(Thing):
            pass

        class Ability_score(pzo2101.Characteristic):
            pass

        class ability_boost(Character_backbone_feat >> Ability_score):
            pass

        class Trait(Thing):
            pass

        class has_trait(Thing >> Trait):
            pass

        class level(Thing >> int, FunctionalProperty):
            pass

        class Heritage(Feat):
            pass

        class prereq(Thing >> Thing):
            pass

        class prereq_details(Thing >> str):
            pass

        class Gameclass(Character_backbone_feat):
            pass

        class additional_skills(Gameclass >> int, FunctionalProperty):
            pass

        class experted(trained):
            pass

        class Class_specialization(Feat):
            pass

        class Background(Character_backbone_feat):
            pass

        class lore_speciality(Background >> str, FunctionalProperty):
            pass

        class Art(Thing):
            pass

        class image(AnnotationProperty):
            namespace = pzo2101.get_namespace("http://schema.org/")

        class depicts(Art >> Thing):
            pass

        class is_depicted_by(ObjectProperty):
            inverse_property = depicts

        class Spellcaster_class(Gameclass):
            pass

        class spells_per_day(Spellcaster_class >> int, FunctionalProperty):
            comment = ("Base count of spells per day, X.\n"
                       "Spells per day: cantrips = 5,  count of n-level spells = {level <= (n-1)*2: 0; level = (2*n - "
                       "1): X - 1; level >= 2*n: X}.")

        class Animal_companion_specialization(Feat):
            comment = "Specialized animal companions are more intelligent and engage in more complex behaviors."

        class Familiar_ability(Feat):
            pass

        class Master_ability(Feat):
            pass

        class abbreviation(AnnotationProperty):
            pass

        class duration(Thing >> str, FunctionalProperty):
            pass

        class range(Thing >> int, FunctionalProperty):
            pass


def fill_characteristics(pzo2101):
    with pzo2101:
        Characteristic = pzo2101.Characteristic

        class changes(Thing >> pzo2101.Characteristic):
            pass

        class Characteristic_with_proficiency(Characteristic):
            pass

        main.fill_onto_from_xml(pzo2101, 'Characteristics', Characteristic)


def fill_abilities(pzo2101):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Ability scores", pzo2101.Ability_score)


def fill_skills(pzo2101):
    with (pzo2101):
        class Skill(pzo2101.Characteristic_with_proficiency):
            comment = ("While your character’s ability scores represent their raw talent and potential, "
                       "skills represent their training and experience at performing certain tasks. Each skill is "
                       "keyed to one of your character’s ability scores and used for an array of related actions. "
                       "Your character’s expertise in a skill comes from several sources, including their background "
                       "and class.")

        class recall_knowledge_specialization(Skill >> str, FunctionalProperty):
            pass

        main.fill_onto_from_xml(pzo2101, "Skills", Skill)


def fill_rules(pzo2101):
    with pzo2101:
        Gamerule = pzo2101.Gamerule

        class calculations(Gamerule >> str):
            pass

        class uses(Gamerule >> Thing):
            pass

        class Check(Gamerule):
            comment = ("When success isn’t certain—whether you’re swinging a sword at a foul beast, attempting to leap "
                       "across a chasm, or straining to remember the name of the earl’s second cousin at a "
                       "soiree—you’ll attempt a check.")
            calculations = ["check delta = check roll - target dc",
                            "check result = {check delta <= -10: critical failure; -10 < check delta < 0: failure; 0 "
                            "<= check delta < 10: success; check delta >= 10: critical success} + {natural 20: + 1 "
                            "step; natural 1: -1 step}"]

        class Check_roll(Gamerule):
            calculations = ["roll = d20 + ability modifier + proficiency bonus + circumstance modifier + status "
                            "modifier + item modifier + untyped penalties",
                            "dc = 10 + ability modifier + proficiency bonus + circumstance modifier + status modifier "
                            "+ item modifier + untyped penalties"]

        class Flat_check(Check):
            comment = ("When the chance something will happen or fail to happen is based purely on chance, "
                       "you’ll attempt a flat check.")
            calculations = 'check roll = d20'

        class uses_roll(uses, Check >> Check_roll, FunctionalProperty):
            pass

        class selects_roll(pzo2101.selects, Check >> Check_roll):
            pass

        class uses_dc(uses, Check >> Gamerule, FunctionalProperty):
            pass

        class selects_dc(pzo2101.selects, Check >> Gamerule):
            pass

        class check_result(Check >> Gamerule):
            pass

        class check_critical_success(check_result):
            pass

        class check_success(check_result):
            pass

        class check_failure(check_result):
            pass

        class check_critical_failure(check_result):
            pass

        class sets(Gamerule >> pzo2101.Characteristic):
            pass

        class blocks(Gamerule >> Gamerule):
            pass

        class modifies(ObjectProperty):
            inverse_property = uses

        class leads_to(Thing >> Gamerule):
            pass

        class Listener(Gamerule):
            pass

        class listens(Listener >> pzo2101.Characteristic):
            pass

        class Attack_check(Check):
            pass

        class Skill_check(Check):
            pass

        main.fill_onto_from_xml(pzo2101, "Rules", Gamerule)

        render_text = main.render_text
        Condition = pzo2101.Condition

        class Condition_changer(Gamerule):
            equivalent_to = [pzo2101.activates.some(Condition) | pzo2101.deactivates.some(Condition)]
            changes = pzo2101[render_text('Active conditions')]

        selects = pzo2101.selects
        ability_mod = pzo2101[render_text('Ability modifier')]
        pzo2101.Ability_score.is_a.append(Inverse(selects).value(ability_mod))
        pzo2101[render_text('Spellcasting ability modifier')].uses.append(ability_mod)
        pzo2101.Characteristic_with_proficiency.is_a.append(Inverse(selects).value(
            pzo2101[render_text('Proficiency bonus')]))
        Check.uses.append(pzo2101[render_text('order of check results')])
        Check_roll.uses.append(pzo2101[render_text('duplicate effects')])
        Check_roll.is_a.append(Inverse(selects_roll).value(pzo2101[render_text('Initiative roll')]))
        pzo2101.Skill.is_a.append(Inverse(selects).value(pzo2101[render_text('Skill roll')]))
        Attack_check.uses_dc = pzo2101[render_text('Armor class')]
        Attack_check.leads_to.append(pzo2101[render_text('Attack a hidden creature')])
        Attack_check.leads_to.append(pzo2101[render_text('Attack a concealed creature')])
        Attack_check.uses.append(pzo2101[render_text('Attack with unsuitable weapon')])
        Check_roll.uses.append(pzo2101[render_text('Reroll')])
        Skill_check.uses_roll = pzo2101[render_text('Skill roll')]


def fill_conditions(pzo2101):
    with pzo2101:
        class Condition(Thing):
            pass

        class activates(Thing >> Condition):
            pass

        class deactivates(Thing >> Condition):
            pass

        main.fill_onto_from_xml(pzo2101, "Conditions", Condition)


def fill_afflictions(pzo2101):
    with pzo2101:
        class Affliction(Thing):
            comment = ("Diseases and poisons are types of afflictions, as are curses and radiation. An affliction can "
                       "infect a creature for a long time, progressing through different and often increasingly "
                       "debilitating stages.")

        class dc(Affliction >> int):
            pass

        class onset(Affliction >> str):
            comment = ("Some afflictions have onset times. For these afflictions, once you fail your initial save, "
                       "you don’t gain the effects for the first stage of the affliction until the onset time has "
                       "elapsed. If this entry is absent, you gain the effects for the first stage (or the second "
                       "stage on a critical failure) immediately upon failing the initial saving throw.")

        pzo2101.duration.comment.append("If an affliction lasts only a limited amount of time, it lists a maximum "
                                        "duration. Once this duration passes, the affliction ends.")

        class Affliction_stage(Affliction):
            pass

        class stage_level(Affliction_stage >> int):
            pass

        class stage(Affliction >> Affliction_stage):
            pass


def fill_general_feats(pzo2101: Ontology):
    with pzo2101:
        Feat = pzo2101.Feat

        class General_feat(Feat): pass

        main.fill_onto_from_xml(pzo2101, "General feats", General_feat)


def fill_traits(pzo2101):
    with pzo2101:
        Trait = pzo2101.Trait

        class Damage_type(Trait):
            pass

        class Damage_type_physical(Damage_type):
            comment = ("Damage dealt by weapons, many physical hazards, and a handful of spells is collectively called "
                       "physical damage.")

        class Damage_type_energy(Damage_type):
            comment = ("Many spells and other magical effects deal energy damage. Energy damage is also dealt from "
                       "effects in the world, such as the biting cold of a blizzard to a raging forest fire.")

        class Damage_type_alignment(Damage_type):
            comment = ("Weapons and effects keyed to a particular alignment. These damage types apply only to "
                       "creatures that have the opposing alignment trait.")

        class Specialization_effect(Trait):
            pass

        main.fill_onto_from_xml(pzo2101, "Traits", Trait)


def fill_alignments(pzo2101):
    with pzo2101:
        class Alignment(pzo2101.Trait): pass

        main.fill_onto_from_xml(pzo2101, "Alignments", Alignment)


def fill_actions(pzo2101):
    with pzo2101:
        class Action(Thing):
            pass

        class need_training(Action >> bool, FunctionalProperty):
            comment = ("Anyone can use a skill’s untrained actions, but you can use trained actions only if you have a "
                       "proficiency rank of trained or better in that skill.")

        class Single_action(Action):
            comment = ("Can be completed in a very short time. They're self-contained, and their effects are generated "
                       "within the span of single action.")
            duration = "single action, 1/3 turn"

        class Activity(Action):
            comment = ("Usually take longer than single action and require multiple actions, which must be spent in  "
                       "succession.")

        class Reaction(Action):
            comment = ("Have triggers, which must be met for you to use the reaction. You can use reaction anytime its "
                       "trigger is met, whether it's you turn or not, 1 reaction per round.")

        class trigger(Reaction >> Thing):
            pass

        class Free_action(Action):
            comment = "Don't cost you any of your actions per turn, nor do they cost your reaction."

        class Encounter_action(Action):
            pass

        class performs(Thing >> Action):
            pass

        main.fill_onto_from_xml(pzo2101, "Actions", Action)

        Encounter_action.is_a.append(Inverse(performs).value(pzo2101[main.render_text('Acting phase of turn')]))
        for cl in [pzo2101.Skill_check, pzo2101.Attack_check]:
            cl.is_a.append(Inverse(trigger).value(pzo2101[main.render_text('Aid')]))
            cl.uses.append(pzo2101[main.render_text('Aid modifier')])


def fill_animal_companions(pzo2101):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, 'Animal companions', pzo2101.Animal_companion)
        main.fill_onto_from_xml(pzo2101, 'Animal companion specializations',
                                pzo2101.Animal_companion_specialization)


def fill_familiar(pzo2101):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Familiar abilities", pzo2101.Familiar_ability)
        main.fill_onto_from_xml(pzo2101, "Master abilities", pzo2101.Master_ability)


def fill_creatures(pzo2101):
    with pzo2101:
        class Creature(pzo2101.Ancestry):
            comment = ("The six humanoid ancestries are far from Golarion’s only inhabitants. Many other creatures "
                       "dwell in the world, some kindly and others cruel, some wild and others organized, "
                       "some anthropomorphic and others completely monstrous. Even creatures that are usually foes of "
                       "civilization, and whom brave adventurers face in battle, can sometimes be reasoned with or "
                       "even befriended. Not all of them are evil, and some are actively helpful to their neighbors. "
                       "And some, of course, simply want to be left alone.")

        main.fill_onto_from_xml(pzo2101, "Creatures", Creature)


def fill_props(pzo2101: Ontology):
    with pzo2101:
        Ancestry = pzo2101.Playable_ancestry
        Ancestry.comment.append(
            "Your character’s ancestry determines which people they call their own, whether it’s diverse "
            "and ambitious humans, insular but vivacious elves, traditionalist and family-focused dwarves, "
            "or any of the other folk who call Golarion home. A character’s ancestry and their experiences "
            "prior to their life as an adventurer—represented by a background—might be key parts of their "
            "identity, shape how they see the world, and help them find their place in it.")
        Ancestry.has_feat.append(pzo2101.common_language)
        Ancestry.has_selectable_feat.append(pzo2101.local_language)

        class ability_flaw(Ancestry >> pzo2101.Ability_score): pass

        main.fill_onto_from_xml(pzo2101, "Ancestries", Ancestry)

        pzo2101.Language_common.selectable_feat_of.append(pzo2101.human)
        tHumanoid = pzo2101.Trait(main.render_text('humanoid', 'Trait'))
        Ancestry.has_trait.append(tHumanoid)


def fill_feats(pzo2101: Ontology):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Ancestry feats", pzo2101.Feat)


def fill_languages(pzo2101: Ontology):
    with pzo2101:
        class Language(pzo2101.Feat):
            comment = ["The people of the Inner Sea region speak dozens of different languages, along with hundreds "
                       "of dialects and regional variations. While a character can generally get by with Taldane, "
                       "also known as Common, knowing another language is vital in some regions. Being able to speak "
                       "these tongues can help you with negotiation, spying on enemies, or just conducting simple "
                       "commerce. Languages also afford you the chance to contextualize your character in the world "
                       "and give meaning to your other character choices."]

        main.fill_onto_from_xml(pzo2101, "Languages", Language)

        pzo2101['Language_regional'].relates_to.append(pzo2101[main.render_text('local', 'Language')])
        pzo2101[main.render_text('Taldane', 'Language')].equivalent_to.append(
            pzo2101[main.render_text('Common', 'Language')])


def fill_backgrounds(pzo2101):
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


def fill_equipment_hierarchy(pzo2101):
    with pzo2101:
        class Equipment(Thing):
            comment = ("To make your mark on the world, you’ll need to have the right equipment, including armor, "
                       "weapons, and other gear. The various equipment that you can purchase during character "
                       "creation. You can usually find these items for sale in most cities and other large "
                       "settlements.")

        class price(Equipment >> str, FunctionalProperty): pass

        class bulk(Equipment >> str, FunctionalProperty):
            comment = ("As a general rule, an item that weighs 5 to 10 pounds is 1 Bulk, an item weighing less than a "
                       "few ounces is negligible, and anything in between is light. Particularly awkward or unwieldy "
                       "items might have higher Bulk values.")

        class hardness(Equipment >> int, FunctionalProperty): pass

        Equipment("coin", price = "100 cp = 10 sp = 1 gp = 1/10 pp",
                  bulk = "A thousand coins of any denomination or combination of denominations count as 1 Bulk.")

        class Defense_equipment(Equipment): pass

        class ac_bonus(Defense_equipment >> int, FunctionalProperty):
            comment = ("This number is the item bonus you add for the armor when determining Armor Class. A shield "
                       "grants a circumstance bonus to AC, but only when the shield is raised.")

        class speed_penalty(Defense_equipment >> int, FunctionalProperty): pass

        class hands(Equipment >> int, FunctionalProperty):
            comment = "Some weapons require one hand to wield, and others require two."


def fill_shield(pzo2101):
    with pzo2101:
        class Shield(pzo2101.Defense_equipment):
            comment = ("A shield can increase your character’s defense beyond the protection their armor provides. "
                       "Your character must be wielding a shield in one hand to make use of it, and it grants its "
                       "bonus to AC only if they use an action to Raise a Shield. This action grants the shield’s "
                       "bonus to AC as a circumstance bonus until their next turn starts. A shield’s Speed penalty "
                       "applies whenever your character is holding the shield, whether they have raised it or not.")

        main.fill_onto_from_xml(pzo2101, "Shields", Shield)


def fill_gear(pzo2101):
    with pzo2101:
        class Gear_and_services(pzo2101.Equipment):
            comment = ("Your character needs all sorts of items both while exploring and in downtime, ranging from "
                       "rations to climbing gear to fancy clothing, depending on the situation.")

        main.fill_onto_from_xml(pzo2101, "Adventuring gear", Gear_and_services)

        for index, row in main.read_text_for_parse("Adventuring_gear_corpus"):
            corpus = row['corpus']
            lst_corpus = corpus.split(":")
            for i in range(1, len(lst_corpus)):
                lst_before = lst_corpus[i - 1].strip().split(".")
                lst = lst_corpus[i].strip().split(".")
                g_name = lst_before[-1].strip()
                g = pzo2101[main.prepare_name(g_name)]
                g.comment.append(f"{''.join(lst[0:-1])}.")


def fill_packs(pzo2101):
    with pzo2101:
        Equipment = pzo2101.Equipment

        class Equipment_pack(Equipment): pass

        class contains(Equipment_pack >> Equipment): pass

        class Starter_kit(Equipment_pack): pass

        main.fill_onto_from_xml(pzo2101, 'Equipment packs', Equipment_pack)
        Starter_kit.contains.append(pzo2101[main.prepare_name("Adventurer’s pack")])


def fill_weapon_groups(pzo2101):
    with pzo2101:
        Weapon_by_group = pzo2101.Weapon_by_group
        for trait in pzo2101.Specialization_effect.instances():
            if any([trait in w.has_trait for w in pzo2101.Weapon.instances()]):
                cl = types.new_class(trait.name.split("_trait")[0].capitalize() + "_group", (Weapon_by_group,))
                cl.equivalent_to.append(pzo2101.has_trait.value(trait))
        dictionary = {
            'Axe': ['slashing', 'sweep'],
            'Bow': ['piercing'],
            'Brawling': ['agile'],
            'Club': ['bludgeoning'],
            'Dart': ['piercing'],
            'Hammer': ['bludgeoning'],
            'Knife': ['agile'],
            'Pick': ['piercing'],
            'Sling': ['bludgeoning', 'propulsive'],
            'Spear': ['piercing']
        }
        for k in dictionary:
            for t in dictionary[k]:
                pzo2101[f"{k}_group"].is_a.append(
                    pzo2101.has_trait.value(pzo2101[main.render_text(t, 'Trait')])
                )


def fill_weapon(pzo2101: Ontology):
    with pzo2101:
        Equipment = pzo2101.Equipment

        class Weapon(Equipment):
            comment = ("Most characters in Pathfinder carry weapons, ranging from mighty warhammers to graceful bows "
                       "to even simple clubs.")

        class Ammunition(Equipment): pass

        class ammunition(Weapon >> Ammunition, FunctionalProperty): pass

        main.fill_onto_from_xml(pzo2101, "Ammunition", Ammunition)

        class Weapon_by_complexity(Weapon): pass

        class damage(Weapon >> str, FunctionalProperty): pass

        class reload(Weapon >> int, FunctionalProperty):
            comment = ("While all weapons need some amount of time to get into position, many ranged weapons also need "
                       "to be loaded and reloaded. This entry indicates how many Interact actions it takes to reload "
                       "such weapons.")

        class Weapon_by_group(pzo2101.Weapon): pass

        main.fill_onto_from_xml(pzo2101, "Weapons", Weapon_by_complexity)


def fill_armor(pzo2101: Ontology):
    with pzo2101:
        class Armor(pzo2101.Defense_equipment):
            comment = ("Armor increases your character’s defenses, but some medium or heavy armor can hamper movement. "
                       "If you want to increase your character’s defense beyond the protection your armor provides, "
                       "they can use a shield. Armor protects your character only while they’re wearing it.")

        class dex_cap(Armor >> int, FunctionalProperty):
            comment = ("This number is the maximum amount of your Dexterity modifier that can apply to your AC while "
                       "you are wearing a given suit of armor.")

        class check_penalty(Armor >> int, FunctionalProperty):
            comment = ("While wearing your armor, you take this penalty to Strength- and Dexterity-based skill checks, "
                       "except for those that have the attack trait. If you meet the armor’s Strength threshold, "
                       "you don’t take this penalty.")

        class str_threshold(Armor >> int, FunctionalProperty):
            comment = ("This entry indicates the Strength score at which you are strong enough to overcome some of the "
                       "armor’s penalties. If your Strength is equal to or greater than this value, you no longer "
                       "take the armor’s check penalty, and you decrease the Speed penalty by 5 feet")

        main.fill_onto_from_xml(pzo2101, "Armor", Armor)
        for armor in Armor.instances():
            traits = armor.has_trait
            if pzo2101.cloth_trait in traits:
                hardness = 1
            elif pzo2101.leather_trait in traits:
                hardness = 4
            else:
                hardness = 9
            armor.hardness = hardness


def fill_archetypes(pzo2101):
    with pzo2101:
        Feat = pzo2101.Feat

        class Archetype(Feat):
            comment = ("There are infinite possible character concepts, but you might find that the feats and skill "
                       "choices from a single class aren’t sufficient to fully realize your character. Archetypes "
                       "allow you to expand the scope of your character’s class.")

        for gc in pzo2101.Gameclass.instances():
            Archetype(main.render_text(gc.name, object_class = "Archetype"))

        main.fill_onto_from_xml(pzo2101, "Archetype feats", Feat)


def fill_rel_class_kits(pzo2101):
    with pzo2101:
        for pack in pzo2101.Starter_kit.instances():
            gameclass_name = pack.name.split("_s_")[0]
            gc = pzo2101[gameclass_name]
            pack.relates_to.append(gc)


def fill_class_props(pzo2101: Ontology):
    with pzo2101:
        Gameclass = pzo2101.Gameclass

        Gameclass.comment.append("Just as your character’s ancestry plays a key role in expressing their identity and "
                                 "worldview, their class indicates the training they have and will improve upon as an "
                                 "adventurer. Choosing your character’s class is perhaps the most important decision you will "
                                 "make for them. Groups of players often create characters whose skills and abilities "
                                 "complement each other mechanically—for example, ensuring your party includes a healer, "
                                 "a combatoriented character, a stealthy character, and someone with command over magic—so you "
                                 "may wish to discuss options with your group before deciding.")

        for k in [pzo2101.perception, pzo2101.fortitude, pzo2101.reflex, pzo2101.will]:
            Gameclass.trained.append(k)

        main.fill_onto_from_xml(pzo2101, "Classes", Gameclass)


def fill_class_weapon(pzo2101: Ontology):
    with pzo2101:
        fist = pzo2101.fist
        Gameclass = pzo2101.Gameclass
        Gameclass.is_a.append(pzo2101.trained.value(fist))
        trained = pzo2101.trained

        wizard = pzo2101.wizard
        for cl in filter(lambda x: x is not wizard, Gameclass.instances()):
            pzo2101.Simple_weapon.is_a.append(Inverse(trained).value(cl))
        for cl in [pzo2101.barbarian, pzo2101.champion, pzo2101.ranger]:
            pzo2101.Martial_weapon.is_a.append(Inverse(trained).value(cl))
        pzo2101.alchemist.trained.append(pzo2101.alchemical_bomb)

        fighter = pzo2101.fighter
        for weapon_cl in [pzo2101.Simple_weapon, pzo2101.Martial_weapon]:
            weapon_cl.is_a.append(Inverse(pzo2101.experted).value(fighter))
        pzo2101.Advanced_weapon.is_a.append(Inverse(trained).value(fighter))
        fighter.experted.append(fist)


def fill_class_armor(pzo2101: Ontology):
    with pzo2101:
        Gameclass = pzo2101.Gameclass
        for arm in pzo2101.Unarmored_as_armor.instances():
            Gameclass.trained.append(arm)
        arm_dict = {
            pzo2101.Light_armor: [pzo2101.alchemist, pzo2101.barbarian, pzo2101.bard, pzo2101.champion, pzo2101.druid,
                                  pzo2101.fighter, pzo2101.ranger, pzo2101.rogue],
            pzo2101.Medium_armor: [pzo2101.alchemist, pzo2101.barbarian, pzo2101.champion, pzo2101.druid,
                                   pzo2101.fighter, pzo2101.ranger],
            pzo2101.Heavy_armor: [pzo2101.champion, pzo2101.fighter],
        }
        for arm_cl in arm_dict:
            for cl in arm_dict[arm_cl]:
                arm_cl.is_a.append(Inverse(pzo2101.trained).value(cl))


def fill_class_feats(pzo2101: Ontology):
    with pzo2101:
        main.fill_onto_from_xml(pzo2101, "Class feats", pzo2101.Feat)
        main.fill_onto_from_xml(pzo2101, "Class specialization feats", pzo2101.Class_specialization)


def fill_spells(pzo2101):
    with pzo2101:
        class Spell(Thing):
            comment = ("With special gestures and utterances, a spellcaster can call forth mystic energies, warp the "
                       "mind, protect themself against danger, or even create something from nothing. Each class has "
                       "its own method of learning, preparing, and casting spells, and every individual spell "
                       "produces a specific effect, so learning new spells gives a spellcaster an increasing array of "
                       "options to accomplish their goals.")

        class Spell_by_magical_tradition(Spell):
            pass

        class Spell_by_school(Spell):
            pass

        for index, row in main.read_text_for_parse("Spell_categories"):
            name = main.render_text(row['name'], "School") if row['category'] == 'school' else main.render_text(
                row['name'], "Tradition")
            category = Spell_by_school if row['category'] == 'school' else Spell_by_magical_tradition
            cl = types.new_class(name, (category,))
            cl.comment = row['comment']

        for index, row in main.read_text_for_parse("Spells_corpus"):
            for spell_text in filter(lambda x: x != "", row['corpus'].split('.')):
                txt = spell_text.split(':')[0].strip()
                name, school_name = re.search(
                    r'(.*)\((.*)\)', txt).groups()
                name = name.strip()
                if len(name.split(' ')[-1]) == 1:
                    name = ' '.join(name.split(' ')[0:-1])
                if name.split(' ')[-1][-1] == ',':
                    name = ' '.join(name.split(' ')[0:-1])
                school = pzo2101.search(is_a = pzo2101.Spell_by_school, iri = f"*{school_name.capitalize()}*").first()
                comment = spell_text.split(':')[1].strip()
                sp = Spell(
                    name = main.render_text(name, "Spell"),
                    comment = comment,
                    level = row['level'],
                )
                sp.is_a.extend([pzo2101[main.render_text(row['tradition'], "Tradition")], school])

        class Ritual(Spell):
            comment = ("A ritual is an esoteric and complex spell that anyone can cast. It takes much longer to cast a "
                       "ritual than a normal spell, but rituals can have more powerful effects.")

        main.fill_onto_from_xml(pzo2101, "Rituals", Ritual)


def fill_locations(pzo2101):
    with pzo2101:
        class Setting(Thing): pass

        f_name = main.prepare_name
        Setting = pzo2101.Setting

        class Location(Setting):
            pass

        class location(Setting >> Location):
            pass

        main.fill_onto_from_xml(pzo2101, "Locations", Location)


def fill_actors(pzo2101):
    with pzo2101:
        f_name = main.prepare_name

        class Actor(pzo2101.Setting): pass

        class Character(Actor): pass

        main.fill_onto_from_xml(pzo2101, 'Characters', Character)

        class Culture(Actor):
            pass

        class ethnicity_of(Culture >> pzo2101.Ancestry, FunctionalProperty):
            pass

        main.fill_onto_from_xml(pzo2101, "Cultures", Culture)
        '''
        for culture_xml in main.iterate_xml_tree("Cultures"):
            culture = Culture(main.render_text(culture_xml.get('name')))
            main.set_relations(pzo2101, culture, culture_xml)
        '''


def fill_events(pzo2101):
    with pzo2101:
        f_name = main.prepare_name

        class Event(pzo2101.Setting): pass

        class after(Event >> Event): pass

        class during(Event >> Event): pass

        class participant(Event >> pzo2101.Actor): pass

        main.fill_onto_from_xml(pzo2101, "Events", Event)


def fill_factions(pzo2101):
    with pzo2101:
        class Faction(pzo2101.Actor):
            comment = ("While nations and faiths command vast resources and control entire regions, they must still "
                       "compete for the loyalty of their followers. In addition to being swayed by church and state, "
                       "many people are influenced by societal groups known as factions. These groups vary wildly in "
                       "size and purpose— from local thieves’ guilds interested only in filling the pockets and "
                       "bellies of their members, to far-reaching, international commercial conglomerates with their "
                       "own private armies.")

        main.fill_onto_from_xml(pzo2101, "Factions", Faction)


def fill_religions(pzo2101):
    with pzo2101:
        class Religion(pzo2101.Actor):
            comment = ("Selection of a deity is critical for certain classes—like champion and cleric—but most "
                       "characters pay respect to at least one deity to find a focus in life and guide their choices, "
                       "especially in times of hardship or need. Some people instead worship a group of deities "
                       "arranged in a pantheon, follow a nondeific religion like the Green Faith, or adhere to a "
                       "specific philosophy. Note that far more deities, religions, and philosophies exist on any "
                       "world, Golarion included, than those detailed below.")

        class Deity(Religion):
            comment = ("Anyone can worship a deity, but those who do so devoutly should take care to pursue the "
                       "faith’s edicts (behaviors the faith encourages) and avoid its anathemas (actions considered "
                       "blasphemous).")

        Alignment = pzo2101.Alignment

        class follower_alignment(Religion >> Alignment): pass

        class alignment(follower_alignment, FunctionalProperty): pass

        class edicts(Religion >> str, FunctionalProperty): pass

        class anathema(Religion >> str, FunctionalProperty): pass

        class divine_font(Deity >> pzo2101.Spell): pass

        class divine_skill(Deity >> pzo2101.Skill, FunctionalProperty): pass

        class favored_weapon(Deity >> pzo2101.Weapon, FunctionalProperty): pass

        class domain(Deity >> pzo2101.Cleric_domain): pass

        class cleric_spell(Deity >> pzo2101.Spell): pass

        for index, row in main.read_text_for_parse('Deities'):
            corpus = row['corpus']
            x = re.search(
                r"(.*) \((.*)\) (.*) Edicts (.*) Anathema (.*) Follower Alignments (.*) Devotee Benefits Divine Font (.*) Divine Skill (.*) Favored Weapon (.*) Domains (.*) Cleric Spells (.*)",
                corpus).groups()
            align = pzo2101.search(is_a = Alignment, abbreviation = x[1]).first()
            aligns = [pzo2101.search(is_a = Alignment, abbreviation = k.strip()).first() for k in x[5].split(',')]
            deity = Deity(
                name = main.prepare_name(x[0]),
                alignment = align,
                comment = x[2],
                edicts = x[3],
                anathema = x[4],
                follower_alignment = aligns,
                divine_font = [pzo2101[main.render_text(k, "Spell")] for k in x[6].split(" or ")],
                divine_skill = pzo2101[main.prepare_name(x[7])],
                favored_weapon = pzo2101[main.prepare_name(x[8])],
                domain = [pzo2101[prepare_name_domain(k)] for k in x[9].split(",")],
                cleric_spell = [pzo2101[main.render_text(k.split(":")[1], "Spell")]
                                for k in x[10].split(",")]
            )

        class Faith(Religion):
            comment = "Of course, faith can express itself in more ways than venerating a single deity—or a deity at all."

        main.fill_onto_from_xml(pzo2101, "Faiths", Faith)
        Alignment.is_a.append(Inverse(follower_alignment).value(pzo2101['atheism']))


def prepare_name_domain(s):
    return f"{main.prepare_name(s)}_domain"


def fill_domains(pzo2101):
    with pzo2101:
        class Cleric_domain(pzo2101.Setting): pass

        Spell = pzo2101.Spell

        class spell(Cleric_domain >> Spell): pass

        main.fill_onto_from_xml(pzo2101, "Domains", Cleric_domain)


def fill_art(pzo2101):
    with pzo2101:
        Art = pzo2101.Art

        for anc in filter(lambda x: x.name != 'human', pzo2101.Playable_ancestry.instances()):
            for i in range(2):
                art_path = f"https://2e.aonprd.com/Images/Ancestries/{anc.name.capitalize()}0{i + 1}.png"
                art = Art(f"art_{anc.name}_{i + 1}", image = [art_path])
                art.depicts.append(anc)

        for heritage in ['Human', 'HalfElf', 'HalfOrc']:
            art_path = f"https://2e.aonprd.com/Images/Ancestries/{heritage}01.png"
            art = Art(f"art_{heritage.lower()}", image = [art_path])
            art.depicts.append(pzo2101.human)

        class Icon(Art):
            pass

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
            n = religion.name.replace('_',
                                      '') if religion.name != 'prophecies_of_kalistrade' else "ProphetsOfKalistrade"

            Icon(
                name = main.render_text(religion.name, "Icon"),
                image = f"https://2e.aonprd.com/Images/Deities/{n}.png",
                depicts = [religion],
            )


def fill_causers(pzo2101):
    with pzo2101:
        class Causer(pzo2101.Gamerule):
            pass

        dying = pzo2101[main.render_text('Dying')]

        class Causer_dying_to_dead(Causer):
            equivalent_to = [pzo2101.changes.value(pzo2101[main.render_text('Active conditions')]) &
                             pzo2101.activates.value(dying)]
            leads_to = pzo2101[main.render_text('Dying to dead listener')]

        class Causer_lose_dying_condition(Causer):
            equivalent_to = [pzo2101.deactivates.value(dying) & (
                    pzo2101.changes.value(pzo2101[main.render_text('hit points')]) |
                    pzo2101.Check
            )]
            leads_to = pzo2101[main.render_text('Lose dying condition listener')]


def fill():
    pzo2101 = get_ontology(
        "https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#")

    create_hierarchy(pzo2101)
    fill_characteristics(pzo2101)
    fill_abilities(pzo2101)
    fill_skills(pzo2101)
    fill_creatures(pzo2101)
    fill_conditions(pzo2101)
    fill_rules(pzo2101)
    fill_causers(pzo2101)
    fill_afflictions(pzo2101)
    fill_general_feats(pzo2101)
    fill_traits(pzo2101)
    fill_alignments(pzo2101)
    fill_languages(pzo2101)
    fill_props(pzo2101)
    fill_feats(pzo2101)
    fill_animal_companions(pzo2101)
    fill_familiar(pzo2101)
    fill_backgrounds(pzo2101)
    fill_equipment_hierarchy(pzo2101)
    fill_armor(pzo2101)
    fill_shield(pzo2101)
    fill_weapon(pzo2101)
    fill_weapon_groups(pzo2101)
    fill_gear(pzo2101)
    fill_packs(pzo2101)
    fill_actions(pzo2101)
    fill_class_props(pzo2101)
    fill_class_weapon(pzo2101)
    fill_class_armor(pzo2101)
    fill_class_feats(pzo2101)
    fill_archetypes(pzo2101)
    fill_rel_class_kits(pzo2101)
    fill_spells(pzo2101)
    fill_locations(pzo2101)
    fill_actors(pzo2101)
    fill_events(pzo2101)
    fill_factions(pzo2101)
    fill_domains(pzo2101)
    fill_religions(pzo2101)
    fill_art(pzo2101)

    return pzo2101

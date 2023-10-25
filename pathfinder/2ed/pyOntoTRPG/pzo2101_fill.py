import os
from owlready2 import *
from pandas._libs.hashtable import Int8Vector
from pyarrow._flight import Action

import main


def create_annotations(pzo2101):
    class relationValue(AnnotationProperty):
        pass

    class relationArgument(AnnotationProperty):
        pass

    class relationPrereq(AnnotationProperty):
        pass

    class relationOrder(AnnotationProperty):
        pass

    class image(AnnotationProperty):
        namespace = pzo2101.get_namespace("http://schema.org/")

    class abbreviation(AnnotationProperty):
        pass


def create_classes_for_trait():
    class Trait(Thing):
        pass

    class DamageType(Trait):
        pass

    class DamageTypePhysical(DamageType):
        comment = ("Damage dealt by weapons, many physical hazards, and a handful of spells is collectively called "
                   "physical damage.")

    class DamageTypeEnergy(DamageType):
        comment = ("Many spells and other magical effects deal energy damage. Energy damage is also dealt from "
                   "effects in the world, such as the biting cold of a blizzard to a raging forest fire.")

    class DamageTypeAlignment(DamageType):
        comment = ("Weapons and effects keyed to a particular alignment. These damage types apply only to "
                   "creatures that have the opposing alignment trait.")

    class SpecializationEffect(Trait):
        pass

    class Alignment(Trait):
        pass


def create_classes_for_gamerule():
    class Gamerule(Thing):
        pass

    class AbilityModifier(Gamerule):
        comment = "An ability modifier represents your raw capabilities and is derived from an ability score."

    class ProficiencyBonus(Gamerule):
        comment = ("When attempting a check that involves something you have some training in, you will also add your "
                   "proficiency bonus. This bonus depends on your proficiency rank.")

    class CheckRoll(Gamerule):
        pass

    class SkillRoll(CheckRoll):
        pass

    class Check(Gamerule):
        comment = ("When success isn’t certain—whether you’re swinging a sword at a foul beast, attempting to leap "
                   "across a chasm, or straining to remember the name of the earl’s second cousin at a "
                   "soiree—you’ll attempt a check.")

    class FlatCheck(Check):
        comment = ("When the chance something will happen or fail to happen is based purely on chance, "
                   "you’ll attempt a flat check.")

    class AttackCheck(Check):
        pass

    class SkillCheck(Check):
        pass

    class Causer(Gamerule):
        pass

    class CauserDyingToDead(Causer):
        pass

    class CauserLoseDyingCondition(Causer):
        pass

    class CauserSpendAir(Causer):
        pass

    class AreaRule(Gamerule):
        pass


def create_classes_for_feat():
    class Feat(Thing):
        comment = ("All kinds of experiences and training can shape your character beyond what you learn by "
                   "advancing in your class. Abilities that require a degree of training but can be learned by "
                   "anyone—not only members of certain ancestries or classes—are called general feats.")

    class GeneralFeat(Feat):
        pass

    class CharacterBackboneFeat(Feat):
        pass

    class Ancestry(CharacterBackboneFeat):
        pass

    class Creature(Ancestry):
        comment = ("The six humanoid ancestries are far from Golarion’s only inhabitants. Many other creatures "
                   "dwell in the world, some kindly and others cruel, some wild and others organized, "
                   "some anthropomorphic and others completely monstrous. Even creatures that are usually foes of "
                   "civilization, and whom brave adventurers face in battle, can sometimes be reasoned with or "
                   "even befriended. Not all of them are evil, and some are actively helpful to their neighbors. "
                   "And some, of course, simply want to be left alone.")

    class PlayableAncestry(Ancestry):
        comment = ("Your character’s ancestry determines which people they call their own, whether it’s diverse and "
                   "ambitious humans, insular but vivacious elves, traditionalist and family-focused dwarves, "
                   "or any of the other folk who call Golarion home. A character’s ancestry and their experiences "
                   "prior to their life as an adventurer—represented by a background—might be key parts of their "
                   "identity, shape how they see the world, and help them find their place in it.")

    class AnimalCompanion(Ancestry):
        comment = "An animal companion is a loyal comrade who follows your orders."

    class Gameclass(CharacterBackboneFeat):
        comment = ("Just as your character’s ancestry plays a key role in expressing their identity and worldview, "
                   "their class indicates the training they have and will improve upon as an adventurer. Choosing "
                   "your character’s class is perhaps the most important decision you will make for them. Groups of "
                   "players often create characters whose skills and abilities complement each other mechanically—for "
                   "example, ensuring your party includes a healer, a combatoriented character, a stealthy character, "
                   "and someone with command over magic—so you may wish to discuss options with your group before "
                   "deciding.")

    class SpellcasterClass(Gameclass):
        pass

    class Background(CharacterBackboneFeat):
        comment = ("Backgrounds allow you to customize your character based on their life before adventuring. This is "
                   "the next step in their life story after their ancestry, which reflects the circumstances of their "
                   "birth. Your character’s background can help you learn or portray more about their personality "
                   "while also suggesting what sorts of things they’re likely to know. Consider what events set your "
                   "character on their path to the life of an adventurer and how those circumstances relate to their "
                   "background.")

    class Heritage(Feat):
        pass

    class ClassSpecialization(Feat):
        pass

    class AnimalCompanionSpecialization(Feat):
        comment = "Specialized animal companions are more intelligent and engage in more complex behaviors."

    class FamiliarAbility(Feat):
        pass

    class MasterAbility(Feat):
        pass

    class Language(Feat):
        comment = ["The people of the Inner Sea region speak dozens of different languages, along with hundreds "
                   "of dialects and regional variations. While a character can generally get by with Taldane, "
                   "also known as Common, knowing another language is vital in some regions. Being able to speak "
                   "these tongues can help you with negotiation, spying on enemies, or just conducting simple "
                   "commerce. Languages also afford you the chance to contextualize your character in the world "
                   "and give meaning to your other character choices."]

    class Archetype(Feat):
        comment = ("There are infinite possible character concepts, but you might find that the feats and skill "
                   "choices from a single class aren’t sufficient to fully realize your character. Archetypes "
                   "allow you to expand the scope of your character’s class.")

    class Size(Feat):
        pass


def create_classes_for_equipment():
    class Equipment(Thing):
        comment = ("To make your mark on the world, you’ll need to have the right equipment, including armor, "
                   "weapons, and other gear. The various equipment that you can purchase during character "
                   "creation. You can usually find these items for sale in most cities and other large "
                   "settlements.")

    class DefenseEquipment(Equipment):
        pass

    class Armor(DefenseEquipment):
        comment = ("Armor increases your character’s defenses, but some medium or heavy armor can hamper movement. "
                   "If you want to increase your character’s defense beyond the protection your armor provides, "
                   "they can use a shield. Armor protects your character only while they’re wearing it.")

    class UncomfortableArmor(Armor):
        pass

    class LightArmor(UncomfortableArmor):
        pass

    class MediumArmor(UncomfortableArmor):
        pass

    class HeavyArmor(UncomfortableArmor):
        pass

    class Shield(DefenseEquipment):
        comment = ("A shield can increase your character’s defense beyond the protection their armor provides. "
                   "Your character must be wielding a shield in one hand to make use of it, and it grants its "
                   "bonus to AC only if they use an action to Raise a Shield. This action grants the shield’s "
                   "bonus to AC as a circumstance bonus until their next turn starts. A shield’s Speed penalty "
                   "applies whenever your character is holding the shield, whether they have raised it or not.")

    class Weapon(Equipment):
        comment = ("Most characters in Pathfinder carry weapons, ranging from mighty warhammers to graceful bows "
                   "to even simple clubs.")

    class Ammunition(Equipment):
        pass

    class WeaponByComplexity(Weapon):
        pass

    class WeaponByGroup(Weapon):
        pass

    class GearAndServices(Equipment):
        comment = ("Your character needs all sorts of items both while exploring and in downtime, ranging from "
                   "rations to climbing gear to fancy clothing, depending on the situation.")

    class EquipmentPack(Equipment):
        pass

    class Starter_kit(EquipmentPack):
        pass


def create_classes_for_action():
    class Action(Thing):
        pass

    class Activity(Action):
        comment = ("Usually take longer than single action and require multiple actions, which must be spent in  "
                   "succession.")

    class ExplorationActivity(Activity):
        pass

    class EncounterAction(Action):
        pass

    class SingleAction(EncounterAction):
        comment = ("Can be completed in a very short time. They're self-contained, and their effects are generated "
                   "within the span of single action.")

    class Reaction(EncounterAction):
        comment = ("Have triggers, which must be met for you to use the reaction. You can use reaction anytime its "
                   "trigger is met, whether it's you turn or not, 1 reaction per round.")

    class FreeAction(EncounterAction):
        comment = "Don't cost you any of your actions per turn, nor do they cost your reaction."

    class FreeActionWithoutTrigger(FreeAction):
        pass

    class MoveAction(Action):
        pass

    class MoveActionWithAttackOpportunityTrigger(MoveAction):
        pass

    class AttackAction(Action):
        pass

    class ManipulateAction(Action):
        pass

    class ManipulateActionWithAttackOpportunityTrigger(ManipulateAction):
        pass


def create_classes_for_spell():
    class Spell(Thing):
        comment = ("With special gestures and utterances, a spellcaster can call forth mystic energies, warp the "
                   "mind, protect themself against danger, or even create something from nothing. Each class has "
                   "its own method of learning, preparing, and casting spells, and every individual spell "
                   "produces a specific effect, so learning new spells gives a spellcaster an increasing array of "
                   "options to accomplish their goals.")

    class SpellByMagicalTradition(Spell):
        pass

    class SpellBySchool(Spell):
        pass

    class Ritual(Spell):
        comment = ("A ritual is an esoteric and complex spell that anyone can cast. It takes much longer to cast a "
                   "ritual than a normal spell, but rituals can have more powerful effects.")


def create_classes_for_setting():
    class Setting(Thing):
        pass

    class Location(Setting):
        pass

    class Agent(Setting):
        pass

    class Character(Agent):
        pass

    class Culture(Agent):
        pass

    class Event(Setting):
        pass

    class Faction(Agent):
        comment = ("While nations and faiths command vast resources and control entire regions, they must still "
                   "compete for the loyalty of their followers. In addition to being swayed by church and state, "
                   "many people are influenced by societal groups known as factions. These groups vary wildly in "
                   "size and purpose— from local thieves’ guilds interested only in filling the pockets and "
                   "bellies of their members, to far-reaching, international commercial conglomerates with their "
                   "own private armies.")

    class ClericDomain(Setting):
        pass

    class Religion(Agent):
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

    class Faith(Religion):
        comment = "Of course, faith can express itself in more ways than venerating a single deity—or a deity at all."


def create_classes():
    class Statement(Thing):
        pass

    class Art(Thing):
        pass

    class Icon(Art):
        pass

    class Map(Art):
        pass

    class Affliction(Thing):
        comment = ("Diseases and poisons are types of afflictions, as are curses and radiation. An affliction can "
                   "infect a creature for a long time, progressing through different and often increasingly "
                   "debilitating stages.")

    class AfflictionStage(Affliction):
        pass

    class Characteristic(Thing):
        pass

    class Condition(Characteristic):
        comment = ("[condition value, remained duration or permanent]. Activate|deactivate condition = +1|-1 to "
                   "condition value. Change condition = -1 to duration if not permanent.")

    class RelativeCondition(Condition):
        comment = ["you might simultaneously have condition against one creature and not another", "list of targets"]

    class DetectionCondition(Condition):
        comment = "List of target characters. Activate|deactivate condition = add|remove target to list|from the list."

    class CoverCondition(RelativeCondition):
        comment = ("When you’re behind an obstacle that could block weapons, guard you against explosions, and make "
                   "you harder to detect, you’re behind cover.")

    class AbilityScore(Characteristic):
        pass

    class CharacteristicWithProficiency(Characteristic):
        pass

    class Skill(CharacteristicWithProficiency):
        comment = ("While your character’s ability scores represent their raw talent and potential, "
                   "skills represent their training and experience at performing certain tasks. Each skill is "
                   "keyed to one of your character’s ability scores and used for an array of related actions. "
                   "Your character’s expertise in a skill comes from several sources, including their background "
                   "and class.")

    create_classes_for_trait()
    create_classes_for_gamerule()
    create_classes_for_feat()
    create_classes_for_equipment()
    create_classes_for_action()
    create_classes_for_spell()
    create_classes_for_setting()


def create_object_properties_for_gamerule(pzo2101):
    class uses(pzo2101.Gamerule >> Thing):
        pass

    class modifies(Thing >> Thing):
        inverse_property = uses

    class usesRoll(uses, pzo2101.Check >> pzo2101.CheckRoll, FunctionalProperty):
        pass

    class selectsRoll(pzo2101.selects, pzo2101.Check >> pzo2101.CheckRoll):
        pass

    class usesDC(uses, pzo2101.Check >> pzo2101.Gamerule, FunctionalProperty):
        pass

    class selectsDC(pzo2101.selects, pzo2101.Check >> pzo2101.Gamerule):
        pass

    class leadsTo(Thing >> pzo2101.Gamerule):
        comment = "last in order"

    class leadsToElse(leadsTo):
        pass

    class checkCriticalSuccess(leadsTo, pzo2101.Check >> pzo2101.Gamerule):
        pass

    class checkSuccess(leadsTo, pzo2101.Check >> pzo2101.Gamerule):
        pass

    class checkFailure(leadsTo, pzo2101.Check >> pzo2101.Gamerule):
        pass

    class checkCriticalFailure(leadsTo, pzo2101.Check >> pzo2101.Gamerule):
        pass

    class sets(pzo2101.Gamerule >> pzo2101.Characteristic):
        pass

    class blocks(pzo2101.Gamerule >> Thing):
        pass

    class disrupts(pzo2101.Gamerule >> pzo2101.Action):
        pass


def create_object_properties_for_setting(pzo2101):
    Event = pzo2101.Event
    Deity = pzo2101.Deity

    class location(pzo2101.Setting >> pzo2101.Location):
        pass

    class ethnicityOf(pzo2101.Culture >> pzo2101.Ancestry, FunctionalProperty):
        pass

    class after(Event >> Event):
        pass

    class during(Event >> Event):
        pass

    class participant(Event >> pzo2101.Agent):
        pass

    class spell(pzo2101.ClericDomain >> pzo2101.Spell):
        pass

    class followerAlignment(pzo2101.Religion >> pzo2101.Alignment):
        pass

    class alignment(followerAlignment, FunctionalProperty):
        pass

    class divineFont(Deity >> pzo2101.Spell):
        pass

    class divineSkill(Deity >> pzo2101.Skill, FunctionalProperty):
        pass

    class favoredWeapon(Deity >> pzo2101.Weapon, FunctionalProperty):
        pass

    class domain(Deity >> pzo2101.ClericDomain):
        pass

    class clericSpell(Deity >> pzo2101.Spell):
        pass


def create_object_properties(pzo2101):
    class statementEntity(pzo2101.Statement >> Thing):
        pass

    class depicts(pzo2101.Art >> Thing):
        pass

    class isDepictedBy(ObjectProperty):
        inverse_property = depicts

    class selects(Thing >> Thing):
        pass

    class relatesTo(Thing >> Thing, SymmetricProperty):
        pass

    class hasFeat(pzo2101.Feat >> pzo2101.Feat):
        pass

    class featOf(ObjectProperty):
        inverse_property = hasFeat

    class trained(pzo2101.Feat >> Thing):
        pass

    class experted(trained):
        pass

    class abilityBoost(pzo2101.CharacterBackboneFeat >> pzo2101.AbilityScore):
        pass

    class abilityFlaw(pzo2101.PlayableAncestry >> pzo2101.AbilityScore):
        pass

    class trait(Thing >> pzo2101.Trait):
        pass

    class prereq(Thing >> Thing):
        comment = "activated condition or true statement"

    class changes(Thing >> pzo2101.Characteristic):
        comment = "changes value of characteristic or -1 to duration of condition"

    class activates(Thing >> pzo2101.Condition):
        comment = "+1 to value of condition"

    class deactivates(Thing >> pzo2101.Condition):
        comment = "-1 to value of condition to minimum 0"

    class stage(pzo2101.Affliction >> pzo2101.AfflictionStage):
        pass

    class ammunition(pzo2101.Weapon >> pzo2101.Ammunition, FunctionalProperty):
        pass

    class contains(pzo2101.EquipmentPack >> pzo2101.Equipment):
        pass

    class needTraining(pzo2101.Action >> bool, FunctionalProperty):
        comment = ("Anyone can use a skill’s untrained actions, but you can use trained actions only if you have a "
                   "proficiency rank of trained or better in that skill.")

    class trigger(pzo2101.Reaction >> Thing):
        pass

    class performs(Thing >> pzo2101.Action):
        pass

    class space(pzo2101.Size >> str):
        comment = ("The Space entry lists how many feet on a side a creature’s space is, so a Large creature fills a "
                   "10-foot-by-10-foot space (4 squares on the grid).")

    create_object_properties_for_gamerule(pzo2101)
    create_object_properties_for_setting(pzo2101)


def create_data_properties_for_feat(pzo2101):
    class hp(pzo2101.CharacterBackboneFeat >> int, FunctionalProperty):
        comment = 'hit points'
        abbreviation = 'hp'

    class size(pzo2101.Ancestry >> pzo2101.Size, FunctionalProperty):
        pass

    class largerThan(pzo2101.Size >> pzo2101.Size):
        pass

    class speed(pzo2101.Ancestry >> int, FunctionalProperty):
        comment = "land speed in feet"

    class specialSpeed(pzo2101.Ancestry >> str, FunctionalProperty):
        comment = "speed different from land speed, {type of speed: value}"

    class additionalSkills(pzo2101.Gameclass >> int, FunctionalProperty):
        pass

    class loreSpeciality(pzo2101.Background >> str, FunctionalProperty):
        pass

    class spellsPerDay(pzo2101.SpellcasterClass >> int, FunctionalProperty):
        comment = ("Base count of spells per day, X.\n"
                   "Spells per day: cantrips = 5,  count of n-level spells = {level <= (n-1)*2: 0; level = (2*n - "
                   "1): X - 1; level >= 2*n: X}.")


def create_data_properties_for_equipment(pzo2101):
    Equipment = pzo2101.Equipment
    Armor = pzo2101.Armor
    DefenseEquipment = pzo2101.DefenseEquipment
    Weapon = pzo2101.Weapon

    class price(Equipment >> str, FunctionalProperty):
        pass

    class bulk(Equipment >> str, FunctionalProperty):
        comment = ("As a general rule, an item that weighs 5 to 10 pounds is 1 Bulk, an item weighing less than a "
                   "few ounces is negligible, and anything in between is light. Particularly awkward or unwieldy "
                   "items might have higher Bulk values.")

    class hardness(Equipment >> int, FunctionalProperty):
        pass

    class hands(Equipment >> int, FunctionalProperty):
        comment = "Some weapons require one hand to wield, and others require two."

    class acBonus(DefenseEquipment >> int, FunctionalProperty):
        comment = ("This number is the item bonus you add for the armor when determining Armor Class. A shield "
                   "grants a circumstance bonus to AC, but only when the shield is raised.")

    class speedPenalty(DefenseEquipment >> int, FunctionalProperty):
        pass

    class dexCap(Armor >> int, FunctionalProperty):
        comment = ("This number is the maximum amount of your Dexterity modifier that can apply to your AC while "
                   "you are wearing a given suit of armor.")

    class checkPenalty(Armor >> int, FunctionalProperty):
        comment = ("While wearing your armor, you take this penalty to Strength- and Dexterity-based skill checks, "
                   "except for those that have the attack trait. If you meet the armor’s Strength threshold, "
                   "you don’t take this penalty.")

    class strengthThreshold(Armor >> int, FunctionalProperty):
        comment = ("This entry indicates the Strength score at which you are strong enough to overcome some of the "
                   "armor’s penalties. If your Strength is equal to or greater than this value, you no longer "
                   "take the armor’s check penalty, and you decrease the Speed penalty by 5 feet")

    class damage(Weapon >> str, FunctionalProperty):
        pass

    class reload(Weapon >> int, FunctionalProperty):
        comment = ("While all weapons need some amount of time to get into position, many ranged weapons also need "
                   "to be loaded and reloaded. This entry indicates how many Interact actions it takes to reload "
                   "such weapons.")


def create_data_properties(pzo2101):
    create_data_properties_for_feat(pzo2101)
    create_data_properties_for_equipment(pzo2101)

    class statementPredicate(pzo2101.Statement >> str):
        pass

    class statementValue(pzo2101.Statement >> str):
        pass

    class level(Thing >> int, FunctionalProperty):
        pass

    class prereqDetails(Thing >> str):
        pass

    class duration(Thing >> str, FunctionalProperty):
        comment = ("If an affliction lasts only a limited amount of time, it lists a maximum duration. Once this "
                   "duration passes, the affliction ends.")

    class perDay(Thing >> str, FunctionalProperty):
        pass

    class distance(Thing >> str, FunctionalProperty):
        comment = "in feet by default"

    class recallKnowledgeSpecialization(pzo2101.Skill >> str, FunctionalProperty):
        pass

    class calculations(pzo2101.Gamerule >> str):
        pass

    class dc(Thing >> str):
        pass

    class onset(pzo2101.Affliction >> str):
        comment = ("Some afflictions have onset times. For these afflictions, once you fail your initial save, "
                   "you don’t gain the effects for the first stage of the affliction until the onset time has "
                   "elapsed. If this entry is absent, you gain the effects for the first stage (or the second "
                   "stage on a critical failure) immediately upon failing the initial saving throw.")

    class stageLevel(pzo2101.AfflictionStage >> int):
        pass

    class edicts(pzo2101.Religion >> str, FunctionalProperty):
        pass

    class anathema(pzo2101.Religion >> str, FunctionalProperty):
        pass


def create_hierarchy(pzo2101):
    create_annotations(pzo2101)
    create_classes()
    create_object_properties(pzo2101)
    create_data_properties(pzo2101)


def fill_from_xml(pzo2101):
    directory = os.fsencode(main.get_resource_path(''))
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'):
            name = filename[0:-4]
            main.fill_onto_from_xml(pzo2101, name, pzo2101[name])


def fill_from_corpus(pzo2101):
    for index, row in main.read_text_for_parse('Backgrounds'):
        x = re.search(
            r'(.*) BACKGROUND (.*) Choose two ability boosts. One must be to (.*) or (.*), and one is a free ability boost. You’re trained in the (.*) skill and (.*). You gain the (.*) skill feat.',
            row['description']).groups()
        pzo2101.Background(
            main.prepare_name(x[0]),
            comment = x[1],
            abilityBoost = [
                pzo2101.search(is_a = pzo2101.AbilityScore, iri = main.iri_for_search(x[2])).first(),
                pzo2101.search(is_a = pzo2101.AbilityScore, iri = main.iri_for_search(x[3])).first(),
            ],
            trained = pzo2101.search(is_a = pzo2101.Skill, iri = main.iri_for_search(x[4])),
            loreSpeciality = x[5],
            hasFeat = pzo2101.search(is_a = pzo2101.SkillFeat, iri = main.iri_for_search(x[6])),
        )
    for index, row in main.read_text_for_parse("Adventuring_gear_corpus"):
        corpus = row['corpus']
        lst_corpus = corpus.split(":")
        for i in range(1, len(lst_corpus)):
            lst_before = lst_corpus[i - 1].strip().split(".")
            lst = lst_corpus[i].strip().split(".")
            g_name = lst_before[-1].strip()
            g = pzo2101[main.prepare_name(g_name)]
            g.comment.append(f"{''.join(lst[0:-1])}.")
    for index, row in main.read_text_for_parse("Spell_categories"):
        name = main.get_id(row['name'], "School") if row['category'] == 'school' else main.get_id(
            row['name'], "Tradition")
        category = pzo2101.SpellBySchool if row['category'] == 'school' else pzo2101.SpellByMagicalTradition
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
            school = pzo2101.search(is_a = pzo2101.SpellBySchool, iri = f"*{school_name.capitalize()}*").first()
            comment = spell_text.split(':')[1].strip()
            sp = pzo2101.Spell(
                name = main.get_id(name, "Spell"),
                comment = comment,
                level = row['level'],
            )
            sp.is_a.extend([pzo2101[main.get_id(row['tradition'], "Tradition")], school])
    for index, row in main.read_text_for_parse('Deities'):
        corpus = row['corpus']
        x = re.search(
            r"(.*) \((.*)\) (.*) Edicts (.*) Anathema (.*) Follower Alignments (.*) Devotee Benefits Divine Font (.*) Divine Skill (.*) Favored Weapon (.*) Domains (.*) Cleric Spells (.*)",
            corpus).groups()
        align = pzo2101.search(is_a = pzo2101.Alignment, abbreviation = x[1]).first()
        aligns = [pzo2101.search(is_a = pzo2101.Alignment, abbreviation = k.strip()).first() for k in x[5].split(',')]
        deity = pzo2101.Deity(
            name = main.prepare_name(x[0]),
            alignment = align,
            comment = x[2],
            edicts = x[3],
            anathema = x[4],
            followerAlignment = aligns,
            divineFont = [pzo2101[main.get_id(k, "Spell")] for k in x[6].split(" or ")],
            divineSkill = pzo2101[main.prepare_name(x[7])],
            favoredWeapon = pzo2101[main.prepare_name(x[8])],
            domain = [pzo2101[main.get_id(k, 'ClericDomain')] for k in x[9].split(",")],
            clericSpell = [pzo2101[main.get_id(k.split(":")[1], "Spell")]
                            for k in x[10].split(",")]
        )


def define_classes_for_gamerule(pzo2101):
    get_id = main.get_id

    for ability in pzo2101.AbilityScore.instances():
        ability_modifier = pzo2101.AbilityModifier(f'{ability.name}_modifier')
        ability_modifier.uses.append(ability)
    ProficiencyBonus = pzo2101.ProficiencyBonus
    ProficiencyBonus.calculations.append('proficiency bonus = (proficiency rank of characteristic) * 2 + level')
    ProficiencyBonus.uses.extend([pzo2101[get_id(k)] for k in ['level of character', 'proficiency rank order']])
    for characteristic in pzo2101.CharacteristicWithProficiency.instances():
        bonus = ProficiencyBonus(f"{characteristic.name.replace('_proficiency', '')}_proficiency_bonus")
        bonus.uses.append(characteristic)
    for skill in pzo2101.Skill.instances():
        skill_roll = pzo2101.SkillRoll(f'{skill.name}_roll')
        ability_modifier = list(filter(lambda x: skill.relatesTo[0] in x.uses, pzo2101.AbilityModifier.instances()))[
            0]
        bonus = list(filter(lambda x: skill in x.uses, ProficiencyBonus.instances()))[0]
        skill_roll.uses.extend([ability_modifier, bonus])

    pzo2101.Check.calculations = [
        "check delta = check roll - target dc",
        "check result = {check delta <= -10: critical failure; -10 < check delta < 0: failure; 0 "
        "<= check delta < 10: success; check delta >= 10: critical success} + {natural 20: + 1 "
        "step; natural 1: -1 step}"]
    pzo2101.CheckRoll.calculations = [
        "roll = d20 + ability modifier + proficiency bonus + circumstance modifier + status "
        "modifier + item modifier + untyped penalties",
        "dc = 10 + ability modifier + proficiency bonus + circumstance modifier + status modifier "
        "+ item modifier + untyped penalties"]
    pzo2101.FlatCheck.calculations = ['check roll = d20']
    pzo2101.Check.uses.append(pzo2101[get_id('order of check results')])
    pzo2101.CheckRoll.uses.append(pzo2101[get_id('duplicate effects')])
    pzo2101.CheckRoll.is_a.append(Inverse(pzo2101.selectsRoll).value(pzo2101[get_id('Initiative roll')]))
    pzo2101.AttackCheck.leadsTo.extend([
        pzo2101[get_id('Attack a hidden creature')],
        pzo2101[get_id('Attack a concealed creature')]])
    pzo2101.AttackCheck.uses.append(pzo2101[get_id('Attack with unsuitable weapon')])
    pzo2101.CheckRoll.uses.append(pzo2101[get_id('Reroll')])
    pzo2101.SkillCheck.usesRoll = pzo2101[get_id('Skill roll')]
    pzo2101.CauserDyingToDead.equivalent_to = [pzo2101.activates.value(pzo2101[get_id('Dying')])]
    pzo2101.CauserDyingToDead.leadsTo = pzo2101[get_id('Dying to dead listener')]
    pzo2101.CauserLoseDyingCondition.equivalent_to = [
        pzo2101.deactivates.value(pzo2101[get_id('Dying')]) &
        (pzo2101.changes.value(pzo2101[get_id('hit points')]) | pzo2101.Check)]
    pzo2101.CauserLoseDyingCondition.leadsTo.append(pzo2101[get_id('Dying to dead listener')])
    pzo2101.CauserSpendAir.equivalent_to = [pzo2101.changes.value(pzo2101[get_id('Hold breath')])]
    pzo2101.CauserSpendAir.leadsTo.append(pzo2101[get_id('Suffocating listener')])
    pzo2101.AreaRule.isDepictedBy.append(pzo2101[get_id('areas', 'Art')])


def define_classes_for_feat(pzo2101):
    render_text = main.get_id
    pzo2101['LanguageRegional'].relatesTo.append(pzo2101[render_text('local', 'Language')])
    pzo2101[render_text('Taldane', 'Language')].equivalent_to.append(
        pzo2101[render_text('Common', 'Language')])
    pzo2101.PlayableAncestry.hasFeat.append(pzo2101.common_language)
    pzo2101.PlayableAncestry.selects.append(pzo2101.local_language)
    pzo2101.LanguageCommon.is_a.append(Inverse(pzo2101.selects).value(pzo2101.human))
    pzo2101.PlayableAncestry.trait.append(pzo2101.Trait(render_text('humanoid', 'Trait')))
    pzo2101.Background.trained.append(pzo2101.lore)
    pzo2101.hermit.trained.append(pzo2101.occultism)
    pzo2101.hermit.comment.append("You’re trained in the Nature or Occultism skill")
    pzo2101.martial_disciple.trained.append(pzo2101.athletics)
    pzo2101.martial_disciple.hasFeat.append(pzo2101.quick_jump)
    pzo2101.martial_disciple.comment.append("You’re trained in your choice of the Acrobatics or Athletics skill. "
                                            "You gain a skill feat: Cat Fall if you chose Acrobatics or Quick "
                                            "Jump if you chose Athletics.")
    pzo2101.scholar.trained.extend([pzo2101.nature, pzo2101.occultism, pzo2101.religion])
    pzo2101.scholar.comment.append("You’re trained in your choice of the Arcana, Nature, Occultism, or Religion "
                                   "skill, and gain the Assurance skill feat in your chosen skill.")
    for k in [pzo2101.perception, pzo2101.fortitude, pzo2101.reflex, pzo2101.will]:
        pzo2101.Gameclass.trained.append(k)


def define_classes_for_equipment(pzo2101):
    pzo2101.Equipment("coin", price = "100 cp = 10 sp = 1 gp = 1/10 pp",
                      bulk = "A thousand coins of any denomination or combination of denominations count as 1 Bulk.")
    for armor in pzo2101.Armor.instances():
        traits = armor.trait
        if pzo2101.cloth_trait in traits:
            hardness = 1
        elif pzo2101.leather_trait in traits:
            hardness = 4
        else:
            hardness = 9
        armor.hardness = hardness
    for trait in pzo2101.SpecializationEffect.instances():
        if any([trait in w.trait for w in pzo2101.Weapon.instances()]):
            cl = types.new_class(trait.name.split("_trait")[0].capitalize() + "Group", (pzo2101.WeaponByGroup,))
            cl.equivalent_to.append(pzo2101.trait.value(trait))
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
            pzo2101[f"{k}Group"].is_a.append(
                pzo2101.trait.value(pzo2101[main.get_id(t, 'Trait')])
            )
    pzo2101.Starter_kit.contains.append(pzo2101[main.get_id("Adventurer’s pack")])

    trained = pzo2101.trained
    fighter = pzo2101.fighter
    pzo2101.Gameclass.is_a.append(trained.value(pzo2101.fist))
    for cl in filter(lambda x: x is not pzo2101.wizard, pzo2101.Gameclass.instances()):
        pzo2101.SimpleWeapon.is_a.append(Inverse(trained).value(cl))
    for cl in [pzo2101.barbarian, pzo2101.champion, pzo2101.ranger]:
        pzo2101.MartialWeapon.is_a.append(Inverse(trained).value(cl))
    pzo2101.alchemist.trained.append(pzo2101.alchemical_bomb)
    for weapon_cl in [pzo2101.SimpleWeapon, pzo2101.MartialWeapon]:
        weapon_cl.is_a.append(Inverse(pzo2101.experted).value(fighter))
    pzo2101.AdvancedWeapon.is_a.append(Inverse(trained).value(fighter))
    fighter.experted.append(pzo2101.fist)

    for arm in pzo2101.UnarmoredAsArmor.instances():
        pzo2101.Gameclass.trained.append(arm)
    arm_dict = {
        pzo2101.LightArmor: [pzo2101.alchemist, pzo2101.barbarian, pzo2101.bard, pzo2101.champion, pzo2101.druid,
                              pzo2101.fighter, pzo2101.ranger, pzo2101.rogue],
        pzo2101.MediumArmor: [pzo2101.alchemist, pzo2101.barbarian, pzo2101.champion, pzo2101.druid,
                               pzo2101.fighter, pzo2101.ranger],
        pzo2101.HeavyArmor: [pzo2101.champion, pzo2101.fighter],
    }
    for arm_cl in arm_dict:
        for cl in arm_dict[arm_cl]:
            arm_cl.is_a.append(Inverse(pzo2101.trained).value(cl))

    for pack in pzo2101.Starter_kit.instances():
        gameclass_name = pack.name.split("_s_")[0]
        gc = pzo2101[gameclass_name]
        pack.relatesTo.append(gc)

    main.add_class_restriction(pzo2101, 'Shield', 'statementEntity',
                               ['Shield'], True, 'Statement')
    main.add_class_restriction(pzo2101, 'UncomfortableArmor', 'statementEntity',
                               ['Sleeping in armor'], True, 'Statement')


def define_classes_for_art(pzo2101):
    Art = pzo2101.Art

    for anc in filter(lambda x: x.name != 'human', pzo2101.PlayableAncestry.instances()):
        for i in range(2):
            art_path = f"https://2e.aonprd.com/Images/Ancestries/{anc.name.capitalize()}0{i + 1}.png"
            art = Art(f"art_{anc.name}_{i + 1}", image = [art_path])
            art.depicts.append(anc)

    for heritage in ['Human', 'HalfElf', 'HalfOrc']:
        art_path = f"https://2e.aonprd.com/Images/Ancestries/{heritage}01.png"
        art = Art(f"art_{heritage.lower()}", image = [art_path])
        art.depicts.append(pzo2101.human)

    for cl in pzo2101.Gameclass.instances():
        pzo2101.Icon(
            name = f"art_{cl.name}_icon",
            image = f"https://2e.aonprd.com/Images/Class/{cl.name.capitalize()}_Icon.png",
            depicts = [cl],
        )

    religions = list(pzo2101.Deity.instances()) + list(pzo2101.Faith.instances())
    religions.remove(pzo2101['atheism'])
    for religion in religions:
        n = religion.name.replace('_',
                                  '') if religion.name != 'prophecies_of_kalistrade' else "ProphetsOfKalistrade"

        pzo2101.Icon(
            name = main.get_id(religion.name, "Icon"),
            image = f"https://2e.aonprd.com/Images/Deities/{n}.png",
            depicts = [religion],
        )


def define_classes_for_action(pzo2101):
    get_id = main.get_id
    SingleAction = pzo2101.SingleAction
    SingleAction.duration = "single action, 1/3 turn"
    pzo2101.EncounterAction.is_a.append(Inverse(pzo2101.performs).value(
        pzo2101[get_id('Acting phase of turn')]))
    without_trigger = pzo2101[get_id('Without trigger', 'Trait')]
    FreeActionWithoutTrigger = pzo2101.FreeActionWithoutTrigger
    FreeActionWithoutTrigger.equivalent_to = [
        pzo2101.FreeAction & pzo2101.trait.value(without_trigger)]
    for action in pzo2101.FreeAction.instances():
        if not action.trigger:
            action.trait.append(without_trigger)
    for cl in [SingleAction, FreeActionWithoutTrigger]:
        cl.is_a.append(Inverse(pzo2101.selects).value(pzo2101[get_id('Ready')]))
    pzo2101.AttackAction.equivalent_to = [pzo2101.trait.value(pzo2101[get_id('Attack', 'Trait')])]
    for subject_name in ['MoveAction', 'AttackAction']:
        main.add_class_restriction(pzo2101, subject_name, 'leadsTo',
                                   ['Deactivation of cover condition'])
    main.add_class_restriction(pzo2101, 'AttackAction', 'leadsTo',
                               ['Spend two air point'])

    pzo2101.MoveAction.equivalent_to = [pzo2101.Action &
                                         pzo2101.trait.value(pzo2101[get_id('Move', 'Trait')])]
    pzo2101.ManipulateAction.equivalent_to = \
        [pzo2101.trait.value(pzo2101[get_id('Manipulate', 'Trait')])]
    trigger_reaction_trait = pzo2101[get_id('Trigger reaction', 'Trait')]
    pzo2101.MoveActionWithAttackOpportunityTrigger.equivalent_to = [
        pzo2101.MoveAction & pzo2101.trait.value(trigger_reaction_trait)]
    pzo2101.ManipulateActionWithAttackOpportunityTrigger.equivalent_to = [
        pzo2101.ManipulateAction & pzo2101.trait.value(trigger_reaction_trait)]
    for action in pzo2101.Action.instances():
        if pzo2101[get_id('Does not trigger reaction', 'Trait')] not in action.trait and (
                any([pzo2101[get_id(k, 'Trait')] in action.trait for k in ['Move', 'Manipulate']])):
            action.trait.append(trigger_reaction_trait)
    main.add_class_restriction(pzo2101, 'MoveActionWithAttackOpportunityTrigger',
                               'statementEntity', ['Attack of opportunity for move actions'],
                               True, 'Statement')
    main.add_class_restriction(pzo2101, 'ManipulateActionWithAttackOpportunityTrigger',
                               'statementEntity', ['Attack of opportunity for manipulate actions'],
                               True, 'Statement')
    main.add_class_restriction(pzo2101, 'ManipulateActionWithAttackOpportunityTrigger',
                               'disrupts', ['Disrupt manipulate action'], True)

    pzo2101.ExplorationActivity.equivalent_to = [
        pzo2101.Action & pzo2101.trait.value(pzo2101[get_id('Exploration', 'Trait')])]


def define_classes_for_condition(pzo2101):
    get_id = main.get_id

    condition_order = ['Unnoticed', 'Undetected', 'Hidden', 'Observed']
    for i in range(len(condition_order) - 1):
        condition_from = pzo2101[get_id(condition_order[i])]
        condition_to = pzo2101[get_id(condition_order[i + 1])]
        label = f'Change detection condition by one step from {condition_from.name} to {condition_to.name}'
        gamerule = pzo2101.Gamerule(
            name = get_id(label),
            label = label,
            deactivates = [condition_from],
            activates = [condition_to],
        )
        pzo2101[get_id('Change detection condition by one step')].selects.append(gamerule)

    main.add_class_restriction(pzo2101, 'CoverCondition', 'modifies',
                               ['Armor class', 'Reflex saving roll', 'Stealth roll'])
    main.add_class_restriction(
        pzo2101, 'CoverCondition', 'deactivates',
        ['Deactivation of cover condition', 'Unconscious', 'Deactivate cover'], True)
    main.add_class_restriction(pzo2101, 'CoverCondition', 'prereq',
                               ['Hide'], True, 'Statement')


def define_classes(pzo2101):
    define_classes_for_gamerule(pzo2101)
    define_classes_for_feat(pzo2101)
    define_classes_for_equipment(pzo2101)
    define_classes_for_art(pzo2101)
    define_classes_for_action(pzo2101)
    define_classes_for_condition(pzo2101)
    for cl in [pzo2101.SkillCheck, pzo2101.AttackCheck]:
        main.add_class_restriction(pzo2101, cl.name, 'trigger', ['Aid'], True)
        main.add_class_restriction(pzo2101, cl.name, 'uses',
                                   ['Aid modifier', 'Aid modifier critical success'])
    main.add_class_restriction(pzo2101, 'Alignment', 'followerAlignment',
                               ['atheism'], True)


def clear_thing_class(pzo2101):
    for entity in pzo2101.individuals():
        if Thing in entity.is_a and len(entity.is_a) > 1:
            entity.is_a.remove(Thing)
        if len(entity.is_a) > 1:
            for cl in list(entity.is_a):
                if any([cl in k.ancestors() and cl != k for k in entity.is_a]):
                    entity.is_a.remove(cl)


def fill():
    pzo2101 = get_ontology(
        "https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#")

    with pzo2101:
        create_hierarchy(pzo2101)
        fill_from_xml(pzo2101)
        fill_from_corpus(pzo2101)
        define_classes(pzo2101)
        clear_thing_class(pzo2101)

    return pzo2101

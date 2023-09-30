from owlready2 import *

import main


def fill(pzo2101):
    with pzo2101:
        f_name = main.prepare_name

        class Gamerule(Thing):
            pass

        class calculations(Gamerule >> str):
            pass

        class uses(Gamerule >> Thing):
            pass

        class Ability_modifier(Gamerule):
            comment = "An ability modifier represents your raw capabilities and is derived from an ability score."

        for abil in pzo2101.Ability_score.instances():
            Ability_modifier(
                name = f"{abil.name}_modifier",
                comment = f"An ability modifier represents your raw capabilities and is derived from an {abil.name} score.",
            )

        class Proficiency_bonus(Gamerule):
            comment = ("When attempting a check that involves something you have some training in, you will also add "
                       "your proficiency bonus. This bonus depends on your proficiency rank.")
            calculations = ["proficiency bonus = proficiency rank * 2 + level"]

        for prof_ch in pzo2101.Characteristic_with_proficiency.instances():
            Proficiency_bonus(
                name = f"{prof_ch.name.replace('_proficiency', '')}_proficiency_bonus",
                uses = [prof_ch],
            )

        class Check(Gamerule):
            comment = ("When success isn’t certain—whether you’re swinging a sword at a foul beast, attempting to leap "
                       "across a chasm, or straining to remember the name of the earl’s second cousin at a "
                       "soiree—you’ll attempt a check.")
            calculations = ["check delta = check roll - target dc",
                            "check result = {check delta <= -10: critical failure; -10 < check delta < 0: failure; 0 "
                            "<= check delta < 10: success; check delta >= 10: critical success} + {natural 20: + 1 "
                            "step; natural 1: -1 step}"]
        class Roll(Gamerule):
            calculations = ("roll = {for check roll: d20; for check dc: 10} + proficiency bonus + circumstance "
                            "modifier + status modifier + item modifier + untyped penalties}")

        class uses_roll(uses, Check >> Roll, FunctionalProperty):
            pass

        class uses_dc(uses, Check >> Gamerule, FunctionalProperty):
            pass

        class Saving_throw(Check):
            comment = ("saving throws measure your ability to shrug off harmful effects in the form of afflictions, "
                       "damage, or conditions.")

        main.fill_onto_from_xml(pzo2101, "Rules", Gamerule)

        Check.uses.append(pzo2101[f_name('order of check results')])
        Roll.uses.append(pzo2101[f_name('duplicate effects')])
        Proficiency_bonus.uses.extend([pzo2101[f_name(k)] for k in ['proficiency rank order', 'level of character']])
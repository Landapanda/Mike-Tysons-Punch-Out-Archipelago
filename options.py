from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class Goal(Choice):
    """
    Decide your goal.
    -**Defeat Super Macho Man**: For those who aren't quite able to beat Mike Tyson. Defeat him by TKO or KO!
    -**KO Super Macho Man**: Defeat Super Macho Man by KO.
    -**Super Macho Man Decision**: Defeat Super Macho Man by decision. Choose the score requirement in Custom Settings.
    -**Defeat Mike Tyson**: Defeat the final boss of the game Mike Tyson via TKO, KO, or Decision!
    -**KO Mike Tyson**: Go for the extra challenge and make Tyson stay down for the 10-count.
    -**Mike Tyson Decision**: Survive all three rounds and beat Mike Tyson via decision.
    """

    display_name = "Goal"

    option_macho = 0
    option_macho_ko = 1
    option_macho_decision = 2
    option_tyson = 3
    option_tyson_ko = 4
    option_tyson_decision = 5

    default = option_tyson


# class IndividualFighter(Toggle):
#     """
#     Changes the items from circuit unlocks to unlocking every fighter individually.
#     **TKO/KO must be on to ensure there are enough checks.**  
#     """

#     display_name = "Individual Fighter Unlocks"

# class TKO_KOToggle(Toggle):
#     """
#     Enables checks for getting TKOs and KOs on every fight as opposed to a single check for winning the fight.
#     **This must be turned on if you have individual fighters on.**
#     """

#     display_name = "TKO/KO Checks"

class DecisionToggle(Toggle):
    """
    **Requires TKO/KO to be enabled as well.**
    Enable winning via decision as checks for all fights with possible decisions.
    """

    display_name = "Decision Checks"

class ForceKO(Toggle):
    """
    Remove the RNG requirement from Mr. Sandman's KO.
    """

    display_name = "Force KOs"

class AddKOs(Toggle):
    """
    Add KOs to the fights that don't have them. Create the conditions in Custom Options.
    As of now, it will make the KO guaranteed once you reach the knockdown condition.
    """

    display_name = "Add KOs"


class AddDecisions(Toggle):
    """
    **Decision Checks must be on.**
    Add Decisions to the fights that don't have them. (Honda 1, Bull 1, Sandman, Macho). 
    Select the score requirement in Custom Options.
    """

    display_name = "Add Decisions"

class TrapChance(Range):
    """
    Percentage chance that the Star filler item is replaced with a Trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0

class TigerKO(Range):
    """
    How many knockdowns are required for Great Tiger's KO.
    """

    display_name = "Tiger KO Condition"

    range_start = 3
    range_end = 6
    default = 4

class BullKO(Range):
    """
    How many knockdowns are required for Bald Bull 1's KO.
    """

    display_name = "Bald Bull 1 KO Condition"

    range_start = 3
    range_end = 6
    default = 6

class HondaDecision(Range):
    """
    Select how many points (in thousands) are required to defeat Piston Honda by decision.
    """

    display_name = "Piston Honda Decision Score (in thousands)"
    range_start = 3
    range_end = 10
    default = 8

class BullDecision(Range):
    """
    Select how many points (in thousands) are required to defeat Bald Bull by decision.
    """

    display_name = "Super Macho Man Decision Score (in thousands)"
    range_start = 3
    range_end = 10
    default = 8

class SandmanDecision(Range):
    """
    Select how many points (in thousands) are required to defeat Mr. Sandman by decision.
    """

    display_name = "Mr. Sandman Decision Score (in thousands)"
    range_start = 3
    range_end = 10
    default = 8

class MachoDecision(Range):
    """
    Select how many points (in thousands) are required to defeat Super Macho Man by decision.
    """

    display_name = "Super Macho Man Decision Score (in thousands)"
    range_start = 3
    range_end = 10
    default = 8

@dataclass
class MTPOOptions(PerGameCommonOptions):
    goal: Goal
    # fighters: IndividualFighter
    # tko_ko: TKO_KOToggle
    decision: DecisionToggle
    force_ko: ForceKO
    add_ko: AddKOs
    add_decision: AddDecisions
    trap_chance: TrapChance
    tiger_ko: TigerKO
    bull_ko: BullKO
    honda_decision: HondaDecision
    bull_decision: BullDecision
    sandman_decision: SandmanDecision
    macho_decision: MachoDecision


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Game Options",
        [Goal, DecisionToggle, ForceKO, AddKOs, AddDecisions, TrapChance],
    ),
    OptionGroup(
        "Custom Options",
        [TigerKO, BullKO, HondaDecision, BullDecision, SandmanDecision, MachoDecision]
    )
]

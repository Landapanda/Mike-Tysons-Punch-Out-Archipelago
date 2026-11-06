from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class Goal(Choice):
    """
    Decide your goal.
    -**Defeat Super Macho Man**: For those who aren't quite able to beat Mike Tyson. Defeat him by TKO or KO!
    -**KO Super Macho Man**: Defeat Super Macho Man by KO.
    -**Defeat Mike Tyson**: Defeat the final boss of the game Mike Tyson via TKO, KO, or Decision!
    -**KO Mike Tyson**: Go for the extra challenge and make Tyson stay down for the 10-count.
    -**Mike Tyson Decision**: Survive all three rounds and beat Mike Tyson via decision.
    """

    display_name = "Goal"

    option_macho = 0
    option_macho_ko = 1
    option_tyson = 2
    option_tyson_ko = 3
    option_tyson_decision = 4

    default = option_tyson



class TrapChance(Range):
    """
    Percentage chance that the Star filler item is replaced with a Trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


# class TKO_KOToggle(Toggle):
#     """
#     Enables checks for getting TKOs and KOs on every fight as opposed to a single check for winning the fight.
#     """

#     display_name = "TKO/KO Checks"

class DecisionToggle(Toggle):
    """
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

@dataclass
class MTPOOptions(PerGameCommonOptions):
    goal: Goal
    decision: DecisionToggle
    force_ko: ForceKO
    add_ko: AddKOs
    trap_chance: TrapChance
    tiger_ko: TigerKO
    bull_ko: BullKO


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Game Options",
        [Goal, DecisionToggle, ForceKO, AddKOs, TrapChance],
    ),
    OptionGroup(
        "Custom Options",
        [TigerKO, BullKO]
    )
]

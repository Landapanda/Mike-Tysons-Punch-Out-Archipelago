from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from .options import Goal

if TYPE_CHECKING:
    from .world import MTPOWorld


def set_all_rules(world: MTPOWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: MTPOWorld) -> None:
    joe_to_kaiser = world.get_entrance("Glass Joe to Von Kaiser")
    kaiser_to_honda = world.get_entrance("Von Kaiser to Piston Honda")
    honda_to_don = world.get_entrance("Piston Honda to Don Flamenco")
    don_to_hippo = world.get_entrance("Don Flamenco to King Hippo")
    hippo_to_tiger = world.get_entrance("King Hippo to Great Tiger")
    tiger_to_bull = world.get_entrance("Great Tiger to Bald Bull")
    bull_to_honda_2 = world.get_entrance("Bald Bull to Piston Honda 2")
    honda_2_to_soda = world.get_entrance("Piston Honda 2 to Soda Popinski")
    soda_to_bull_2 = world.get_entrance("Soda Popinski to Bald Bull 2")
    bull_2_to_don_2 = world.get_entrance("Bald Bull 2 to Don Flamenco 2")
    don_2_to_sandman = world.get_entrance("Don Flamenco 2 to Mr. Sandman")
    sandman_to_macho = world.get_entrance("Mr. Sandman to Super Macho Man")
    if world.options.goal.value > 1:
        macho_to_tyson = world.get_entrance("Super Macho Man to Mike Tyson")

    have_kaiser = Has("Von Kaiser")
    have_honda_1 = Has("Piston Honda")
    have_don_1 = Has("Don Flamenco")
    have_hippo = Has("King Hippo")
    have_tiger = Has("Great Tiger")
    have_bull_1 = Has("Bald Bull")
    have_honda_2: Rule = Has("Piston Honda 2")
    have_soda: Rule = Has("Soda Popinski")
    have_bull_2: Rule = Has("Bald Bull 2")
    have_don_2: Rule = Has("Don Flamenco 2")
    have_sandman: Rule = Has("Mr. Sandman")
    have_macho: Rule = Has("Super Macho Man")
    have_tyson: Rule = Has("Mike Tyson")

    have_round_2: Rule = Has("Progressive Round", count=2)
    can_decision: Rule = Has("Progressive Round", count=3)
    have_stars: Rule = Has("Star Punch Unlock")
    have_heal: Rule = Has("Heal in Between Rounds")

    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.
    # if world.options.hammer:
    #     overworld_to_top_middle_room = world.get_entrance("Overworld to Top Middle Room")
    #     can_smash_brick = Has("Hammer")
    #     world.set_rule(overworld_to_top_middle_room, can_smash_brick)

    world.set_rule(joe_to_kaiser, have_kaiser)
    world.set_rule(kaiser_to_honda, have_honda_1)
    world.set_rule(honda_to_don, have_don_1)
    world.set_rule(don_to_hippo, have_hippo)
    world.set_rule(hippo_to_tiger, have_tiger)
    world.set_rule(tiger_to_bull, have_bull_1)
    world.set_rule(bull_to_honda_2, have_honda_2)
    world.set_rule(honda_2_to_soda, have_soda)
    world.set_rule(soda_to_bull_2, have_bull_2) # & (have_stars | can_decision)
    world.set_rule(bull_2_to_don_2, have_don_2)
    world.set_rule(don_2_to_sandman, have_sandman)
    world.set_rule(sandman_to_macho, have_macho)
    if world.options.goal.value > 1:
        world.set_rule(macho_to_tyson, have_tyson)


def set_all_location_rules(world: MTPOWorld) -> None:
    have_kaiser: Rule = Has("Von Kaiser")
    have_honda_1: Rule = Has("Piston Honda")
    have_don_1: Rule = Has("Don Flamenco")
    have_hippo: Rule = Has("King Hippo")
    have_tiger: Rule = Has("Great Tiger")
    have_bull_1: Rule = Has("Bald Bull")
    have_honda_2: Rule = Has("Piston Honda 2")
    have_soda: Rule = Has("Soda Popinski")
    have_bull_2: Rule = Has("Bald Bull 2")
    have_don_2: Rule = Has("Don Flamenco 2")
    have_sandman: Rule = Has("Mr. Sandman")
    have_macho: Rule = Has("Super Macho Man")
    have_tyson: Rule = Has("Mike Tyson")

    have_round_2: Rule = Has("Progressive Round", count=2)
    can_decision: Rule = Has("Progressive Round", count=3)
    have_stars: Rule = Has("Star Punch Unlock")
    have_heal: Rule = Has("Heal in Between Rounds")

    decision_on: bool = world.options.decision.value
    add_ko: bool = world.options.add_ko.value
    tiger_ko_con = world.options.tiger_ko.value
    bull_ko_con = world.options.bull_ko.value

    kaiser_tko = world.get_location("TKO Von Kaiser")
    world.set_rule(kaiser_tko, have_kaiser)
    kaiser_ko = world.get_location("KO Von Kaiser")
    world.set_rule(kaiser_ko, have_kaiser & have_round_2)
    honda_1_tko = world.get_location("TKO Piston Honda")
    world.set_rule(honda_1_tko, have_honda_1)
    honda_1_ko = world.get_location("KO Piston Honda")
    world.set_rule(honda_1_ko, have_honda_1 & have_round_2)
    don_1_tko = world.get_location("TKO Don Flamenco")
    world.set_rule(don_1_tko, have_don_1)
    don_1_ko = world.get_location("KO Don Flamenco")
    world.set_rule(don_1_ko, have_don_1)
    hippo_defeat = world.get_location("KO King Hippo")
    world.set_rule(hippo_defeat, have_hippo)
    tiger_tko = world.get_location("TKO Great Tiger")
    world.set_rule(tiger_tko, have_tiger)
    bull_1_tko = world.get_location("TKO Bald Bull")
    world.set_rule(bull_1_tko, have_bull_1)
    honda_2_tko = world.get_location("TKO Piston Honda 2")
    world.set_rule(honda_2_tko, have_honda_2)
    honda_2_ko = world.get_location("KO Piston Honda 2")
    world.set_rule(honda_2_ko, have_honda_2)
    soda_tko = world.get_location("TKO Soda Popinski")
    world.set_rule(soda_tko, have_soda)
    soda_ko = world.get_location("KO Soda Popinski")
    world.set_rule(soda_ko, have_soda & can_decision)
    bull_2_tko = world.get_location("TKO Bald Bull 2")
    world.set_rule(bull_2_tko, have_bull_2 & have_stars)
    bull_2_ko = world.get_location("KO Bald Bull 2")
    world.set_rule(bull_2_ko, have_bull_2 & can_decision)
    don_2_tko = world.get_location("TKO Don Flamenco 2")
    world.set_rule(don_2_tko, have_don_2)
    don_2_ko = world.get_location("KO Don Flamenco 2")
    world.set_rule(don_2_ko, have_don_2 & can_decision)
    sandman_tko = world.get_location("TKO Mr. Sandman")
    world.set_rule(sandman_tko, have_sandman)
    sandman_ko = world.get_location("KO Mr. Sandman")
    world.set_rule(sandman_ko, have_sandman & can_decision)
    if decision_on:
        joe_decision = world.get_location("Glass Joe Decision")
        world.set_rule(joe_decision, can_decision)
        kaiser_decision = world.get_location("Von Kaiser Decision")
        world.set_rule(kaiser_decision, have_kaiser & can_decision & have_stars)
        don_1_decision = world.get_location("Don Flamenco Decision")
        world.set_rule(don_1_decision, have_don_1 & can_decision & have_stars)
        tiger_decision = world.get_location("Great Tiger Decision")
        world.set_rule(tiger_decision, have_tiger & can_decision & have_stars)
        honda_2_decision = world.get_location("Piston Honda 2 Decision")
        world.set_rule(honda_2_decision, have_honda_2 & can_decision)
        soda_decision = world.get_location("Soda Popinski Decision")
        world.set_rule(soda_decision, have_soda & can_decision & have_stars)
        bull_2_decision = world.get_location("Bald Bull 2 Decision")
        world.set_rule(bull_2_decision, have_bull_2 & can_decision & have_stars)
        don_2_decision = world.get_location("Don Flamenco 2 Decision")
        world.set_rule(don_2_decision, have_don_2 & can_decision)
    if add_ko:
        tiger_ko = world.get_location("KO Great Tiger")
        bull_ko = world.get_location("KO Bald Bull")
        if tiger_ko_con > 4:
            world.set_rule(tiger_ko, have_tiger & can_decision)
        else:
            world.set_rule(tiger_ko, have_tiger & have_round_2)
        if bull_ko_con > 4:
            world.set_rule(tiger_ko, have_bull_1 & can_decision)
        else:
            world.set_rule(tiger_ko, have_bull_1 & have_round_2)
            


    goal = world.options.goal.value

    if goal == 0:
        macho_defeat = world.get_location("Defeat Super Macho Man")
        world.set_rule(macho_defeat, have_macho)
    elif goal == 1:
        macho_ko = world.get_location("KO Super Macho Man")
        world.set_rule(macho_ko, have_macho & have_round_2)
    elif goal == 2:
        macho_tko = world.get_location("TKO Super Macho Man")
        world.set_rule(macho_tko, have_macho)
        macho_ko = world.get_location("KO Super Macho Man")
        world.set_rule(macho_ko, have_macho & have_round_2)
        tyson_defeat = world.get_location("Defeat Mike Tyson")
        world.set_rule(tyson_defeat, have_tyson)
    elif goal == 3:
        macho_tko = world.get_location("TKO Super Macho Man")
        world.set_rule(macho_tko, have_macho)
        macho_ko = world.get_location("KO Super Macho Man")
        world.set_rule(macho_ko, have_macho & have_round_2)
        tyson_ko = world.get_location("KO Mike Tyson")
        world.set_rule(tyson_ko, have_tyson & can_decision)
    else:
        macho_tko = world.get_location("TKO Super Macho Man")
        world.set_rule(macho_tko, have_macho)
        macho_ko = world.get_location("KO Super Macho Man")
        world.set_rule(macho_ko, have_macho & have_round_2)
        tyson_decision = world.get_location("Mike Tyson Decision")
        world.set_rule(tyson_decision, have_tyson & can_decision)


def set_completion_condition(world: MTPOWorld) -> None:
    if world.options.goal.value > 1:
        world.set_completion_rule(Has("Mike Tyson"))
    else:
        world.set_completion_rule(Has("Super Macho Man"))

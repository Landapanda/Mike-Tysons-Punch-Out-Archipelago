from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import MTPOWorld

def create_and_connect_regions(world: MTPOWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: MTPOWorld) -> None:
    joe = Region("Joe", world.player, world.multiworld)
    kaiser = Region("Kaiser", world.player, world.multiworld)
    honda_1 = Region("Honda", world.player, world.multiworld)
    don_1 = Region("Don", world.player, world.multiworld)
    hippo = Region("Hippo", world.player, world.multiworld)
    tiger = Region("Tiger", world.player, world.multiworld)
    bull_1 = Region("Bull", world.player, world.multiworld)
    honda_2 = Region("Honda2", world.player, world.multiworld)
    soda = Region("Soda", world.player, world.multiworld)
    bull_2 = Region("Bull2", world.player, world.multiworld)
    don_2 = Region("Don2", world.player, world.multiworld)
    sandman = Region("Sandman", world.player, world.multiworld)
    macho = Region("Macho", world.player, world.multiworld)
    
    regions = [joe, kaiser, honda_1, don_1, hippo, tiger, bull_1, honda_2, soda, bull_2, don_2, sandman, macho]

    if world.options.goal.value > 1:
        tyson = Region("Tyson", world.player, world.multiworld)
        regions.append(tyson)

    world.multiworld.regions += regions


def connect_regions(world: MTPOWorld) -> None:
    joe = world.get_region("Joe")
    kaiser = world.get_region("Kaiser")
    honda_1 = world.get_region("Honda")
    don_1 = world.get_region("Don")
    hippo = world.get_region("Hippo")
    tiger = world.get_region("Tiger")
    bull_1 = world.get_region("Bull")
    honda_2 = world.get_region("Honda2")
    soda = world.get_region("Soda")
    bull_2 = world.get_region("Bull2")
    don_2 = world.get_region("Don2")
    sandman = world.get_region("Sandman")
    macho = world.get_region("Macho")
    if world.options.goal.value > 1:
        tyson = world.get_region("Tyson")

    joe_to_kaiser = Entrance(world.player, "Glass Joe to Von Kaiser", parent=joe)
    joe.exits.append(joe_to_kaiser)

    kaiser_to_honda = Entrance(world.player, "Von Kaiser to Piston Honda", parent=kaiser)
    kaiser.exits.append(kaiser_to_honda)

    honda_to_don = Entrance(world.player, "Piston Honda to Don Flamenco", parent=honda_1)
    honda_1.exits.append(honda_to_don)

    don_to_hippo = Entrance(world.player, "Don Flamenco to King Hippo", parent=don_1)
    don_1.exits.append(don_to_hippo)

    hippo_to_tiger = Entrance(world.player, "King Hippo to Great Tiger", parent=hippo)
    hippo.exits.append(hippo_to_tiger)

    tiger_to_bull = Entrance(world.player, "Great Tiger to Bald Bull", parent=tiger)
    tiger.exits.append(tiger_to_bull)

    bull_to_honda_2 = Entrance(world.player, "Bald Bull to Piston Honda 2", parent=bull_1)
    bull_1.exits.append(bull_to_honda_2)

    honda_2_to_soda = Entrance(world.player, "Piston Honda 2 to Soda Popinski", parent=honda_2)
    honda_2.exits.append(honda_2_to_soda)

    soda_to_bull_2 = Entrance(world.player, "Soda Popinski to Bald Bull 2", parent=soda)
    soda.exits.append(soda_to_bull_2)

    bull_2_to_don_2 = Entrance(world.player, "Bald Bull 2 to Don Flamenco 2", parent=bull_2)
    bull_2.exits.append(bull_2_to_don_2)

    don_2_to_sandman = Entrance(world.player, "Don Flamenco 2 to Mr. Sandman", parent=don_2)
    don_2.exits.append(don_2_to_sandman)

    sandman_to_macho = Entrance(world.player, "Mr. Sandman to Super Macho Man", parent=sandman)
    sandman.exits.append(sandman_to_macho)

    if world.options.goal.value > 1:
        macho_to_tyson = Entrance(world.player, "Super Macho Man to Mike Tyson", parent=macho)
        macho.exits.append(macho_to_tyson)

    joe_to_kaiser.connect(kaiser)
    kaiser_to_honda.connect(honda_1)
    honda_to_don.connect(don_1)
    don_to_hippo.connect(hippo)
    hippo_to_tiger.connect(tiger)
    tiger_to_bull.connect(bull_1)
    bull_to_honda_2.connect(honda_2)
    honda_2_to_soda.connect(soda)
    soda_to_bull_2.connect(bull_2)
    bull_2_to_don_2.connect(don_2)
    don_2_to_sandman.connect(sandman)
    sandman_to_macho.connect(macho)
    if world.options.goal.value > 1:
        macho_to_tyson.connect(tyson)

    # An even easier way is to use the region.connect helper.
    # overworld.connect(right_room, "Overworld to Right Room")
    # right_room.connect(final_boss_room, "Right Room to Final Boss Room")

    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    # overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     overworld.connect(top_middle_room, "Overworld to Top Middle Room")

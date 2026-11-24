from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

if TYPE_CHECKING:
    from .world import MTPOWorld

LOCATION_NAME_TO_ID = {
    "TKO Glass Joe": 1,
    "KO Glass Joe": 2,
    "Glass Joe Decision": 3,
    "TKO Von Kaiser": 4,
    "KO Von Kaiser": 5,
    "Von Kaiser Decision": 6,
    "TKO Piston Honda": 7,
    "KO Piston Honda": 8,
    "Piston Honda Decision": 9,
    "TKO Don Flamenco": 10,
    "KO Don Flamenco": 11,
    "Don Flamenco Decision": 12,
    "KO King Hippo": 13,
    "TKO Great Tiger": 14,
    "KO Great Tiger": 15,
    "Great Tiger Decision": 16,
    "TKO Bald Bull": 17,
    "KO Bald Bull": 18,
    "Bald Bull Decision": 19,
    "TKO Piston Honda 2": 20,
    "KO Piston Honda 2": 21,
    "Piston Honda 2 Decision": 22,
    "TKO Soda Popinski": 23,
    "KO Soda Popinski": 24,
    "Soda Popinski Decision": 25,
    "TKO Bald Bull 2": 26,
    "KO Bald Bull 2": 27,
    "Bald Bull 2 Decision": 28,
    "TKO Don Flamenco 2": 29,
    "KO Don Flamenco 2": 30,
    "Don Flamenco 2 Decision": 31,
    "TKO Mr. Sandman": 32,
    "KO Mr. Sandman": 33,
    "Mr. Sandman Decision": 34,
    "Defeat Super Macho Man": 35,
    "TKO Super Macho Man": 36,
    "KO Super Macho Man": 37,
    "Super Macho Man Decision": 38,
    "Defeat Mike Tyson": 39,
    "TKO Mike Tyson": 40,
    "KO Mike Tyson": 41,
    "Mike Tyson Decision": 42
}

class MTPOLocation(Location):
    game = "Mike Tyson's Punch-Out!!"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: MTPOWorld) -> None:
    create_regular_locations(world)


def create_regular_locations(world: MTPOWorld) -> None:
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

    goal = world.options.goal.value
    decision_on: bool = world.options.decision.value
    add_ko: bool = world.options.add_ko.value
    add_decision: bool = world.options.add_decision.value 

    if goal > 1:
        tyson = world.get_region("Tyson")

    joe_locations = get_location_names_with_ids(
        ["TKO Glass Joe", "KO Glass Joe"]
    )

    kaiser_locations = get_location_names_with_ids(
        ["TKO Von Kaiser", "KO Von Kaiser"]
    )

    honda_1_locations = get_location_names_with_ids(
        ["TKO Piston Honda", "KO Piston Honda"]
    )

    don_1_locations = get_location_names_with_ids(
        ["TKO Don Flamenco", "KO Don Flamenco"]
    )

    hippo_locations = get_location_names_with_ids(
        ["KO King Hippo"]
    )

    tiger_locations = get_location_names_with_ids(
        ["TKO Great Tiger"]
    )

    bull_1_locations = get_location_names_with_ids(
        ["TKO Bald Bull"]
    )

    honda_2_locations = get_location_names_with_ids(
        ["TKO Piston Honda 2", "KO Piston Honda 2"]
    )

    soda_locations = get_location_names_with_ids(
        ["TKO Soda Popinski", "KO Soda Popinski"]
    )

    bull_2_locations = get_location_names_with_ids(
        ["TKO Bald Bull 2", "KO Bald Bull 2"]
    )

    don_2_locations = get_location_names_with_ids(
        ["TKO Don Flamenco 2", "KO Don Flamenco 2"]
    )

    sandman_locations = get_location_names_with_ids(
        ["TKO Mr. Sandman", "KO Mr. Sandman"]
    )

    # macho_locations = get_location_names_with_ids(
    #     ["TKO Super Macho Man", "KO Super Macho Man"]
    # )

    # tyson_locations = get_location_names_with_ids(
    #     ["TKO Mike Tyson", "KO Mike Tyson", "Mike Tyson Decision"]
    # )

    macho_locations: dict[str|int] = {}

    tyson_locations: dict[str|int] = {}

    if goal == 0:
        macho_locations.update(get_location_names_with_ids(["Defeat Super Macho Man"]))
    elif goal == 1:
        macho_locations.update(get_location_names_with_ids(["KO Super Macho Man"]))
    elif goal == 2:
        macho_locations.update(get_location_names_with_ids(["Super Macho Man Decision"]))
    elif goal == 3:
        macho_locations.update(get_location_names_with_ids(["TKO Super Macho Man"]))
        macho_locations.update(get_location_names_with_ids(["KO Super Macho Man"]))
        tyson_locations.update(get_location_names_with_ids(["Defeat Mike Tyson"]))
    elif goal == 4:
        macho_locations.update(get_location_names_with_ids(["TKO Super Macho Man"]))
        macho_locations.update(get_location_names_with_ids(["KO Super Macho Man"]))
        tyson_locations.update(get_location_names_with_ids(["KO Mike Tyson"]))
    else:
        macho_locations.update(get_location_names_with_ids(["TKO Super Macho Man"]))
        macho_locations.update(get_location_names_with_ids(["KO Super Macho Man"]))
        tyson_locations.update(get_location_names_with_ids(["Mike Tyson Decision"]))

    if decision_on:
        joe_locations.update(get_location_names_with_ids(["Glass Joe Decision"]))
        kaiser_locations.update(get_location_names_with_ids(["Von Kaiser Decision"]))
        don_1_locations.update(get_location_names_with_ids(["Don Flamenco Decision"]))
        tiger_locations.update(get_location_names_with_ids(["Great Tiger Decision"]))
        honda_2_locations.update(get_location_names_with_ids(["Piston Honda 2 Decision"]))
        soda_locations.update(get_location_names_with_ids(["Soda Popinski Decision"]))
        bull_2_locations.update(get_location_names_with_ids(["Bald Bull 2 Decision"]))
        don_2_locations.update(get_location_names_with_ids(["Don Flamenco 2 Decision"]))
        if add_decision:
            honda_1_locations.update(get_location_names_with_ids(["Piston Honda Decision"]))
            bull_1_locations.update(get_location_names_with_ids(["Bald Bull Decision"]))
            sandman_locations.update(get_location_names_with_ids(["Mr. Sandman Decision"]))
            if goal not in [0, 1, 2]:
                macho_locations.update(get_location_names_with_ids(["Super Macho Man Decision"]))
    if add_ko:
        tiger_locations.update(get_location_names_with_ids(["KO Great Tiger"]))
        bull_1_locations.update(get_location_names_with_ids(["KO Bald Bull"]))


    joe.add_locations(joe_locations, MTPOLocation) 
    kaiser.add_locations(kaiser_locations, MTPOLocation)
    honda_1.add_locations(honda_1_locations, MTPOLocation)
    don_1.add_locations(don_1_locations, MTPOLocation)
    hippo.add_locations(hippo_locations, MTPOLocation)
    tiger.add_locations(tiger_locations, MTPOLocation)
    bull_1.add_locations(bull_1_locations, MTPOLocation)
    honda_2.add_locations(honda_2_locations, MTPOLocation)
    soda.add_locations(soda_locations, MTPOLocation)
    bull_2.add_locations(bull_2_locations, MTPOLocation)
    don_2.add_locations(don_2_locations, MTPOLocation)
    sandman.add_locations(sandman_locations, MTPOLocation)
    macho.add_locations(macho_locations, MTPOLocation)
    if goal > 1:
        tyson.add_locations(tyson_locations, MTPOLocation)

    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     top_middle_room.add_locations(top_middle_room_locations, MTPOLocation)
    # else:
    #     overworld.add_locations(top_middle_room_locations, MTPOLocation)

    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
        # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
        # exist, it must still always be present in the world's location_name_to_id.
        # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
        # bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
        # overworld.add_locations(bottom_left_extra_chest, MTPOLocation)


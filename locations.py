from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items, options

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
    "TKO Don Flamenco": 9,
    "KO Don Flamenco": 10,
    "Don Flamenco Decision": 11,
    "KO King Hippo": 12,
    "TKO Great Tiger": 13,
    "Great Tiger Decision": 14,
    "TKO Bald Bull": 15,
    "TKO Piston Honda 2": 16,
    "KO Piston Honda 2": 17,
    "Piston Honda 2 Decision": 18,
    "TKO Soda Popinski": 19,
    "KO Soda Popinski": 20,
    "Soda Popinski Decision": 21,
    "TKO Bald Bull 2": 22,
    "KO Bald Bull 2": 23,
    "Bald Bull 2 Decision": 24,
    "TKO Don Flamenco 2": 25,
    "KO Don Flamenco 2": 26,
    "Don Flamenco 2 Decision": 27,
    "TKO Mr. Sandman": 28,
    "KO Mr. Sandman": 29,
    "TKO Super Macho Man": 30,
    "KO Super Macho Man": 31,
    "TKO Mike Tyson": 32,
    "KO Mike Tyson": 33,
    "Mike Tyson Decision": 34
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
    tyson = world.get_region("Tyson")

    joe_locations = get_location_names_with_ids(
        ["TKO Glass Joe", "KO Glass Joe", "Glass Joe Decision"]
    )

    kaiser_locations = get_location_names_with_ids(
        ["TKO Von Kaiser", "KO Von Kaiser", "Von Kaiser Decision"]
    )

    honda_1_locations = get_location_names_with_ids(
        ["TKO Piston Honda", "KO Piston Honda"]
    )

    don_1_locations = get_location_names_with_ids(
        ["TKO Don Flamenco", "KO Don Flamenco", "Don Flamenco Decision"]
    )

    hippo_locations = get_location_names_with_ids(
        ["KO King Hippo"]
    )

    tiger_locations = get_location_names_with_ids(
        ["TKO Great Tiger", "Great Tiger Decision"]
    )

    bull_1_locations = get_location_names_with_ids(
        ["TKO Bald Bull"]
    )

    honda_2_locations = get_location_names_with_ids(
        ["TKO Piston Honda 2", "KO Piston Honda 2", "Piston Honda 2 Decision"]
    )

    soda_locations = get_location_names_with_ids(
        ["TKO Soda Popinski", "KO Soda Popinski", "Soda Popinski Decision"]
    )

    bull_2_locations = get_location_names_with_ids(
        ["TKO Bald Bull 2", "KO Bald Bull 2", "Bald Bull 2 Decision"]
    )

    don_2_locations = get_location_names_with_ids(
        ["TKO Don Flamenco 2", "KO Don Flamenco 2", "Don Flamenco 2 Decision"]
    )

    sandman_locations = get_location_names_with_ids(
        ["TKO Mr. Sandman", "KO Mr. Sandman"]
    )

    macho_locations = get_location_names_with_ids(
        ["TKO Super Macho Man", "KO Super Macho Man"]
    )

    # tyson_locations = get_location_names_with_ids(
    #     ["TKO Mike Tyson", "KO Mike Tyson", "Mike Tyson Decision"]
    # )

    tyson_locations: dict[str|int] = {}

    if world.options.goal == "tko":
        tyson_locations.update(get_location_names_with_ids(["TKO Mike Tyson"]))
    elif world.options.goal == "ko":
        tyson_locations.update(get_location_names_with_ids(["KO Mike Tyson"]))
    else:
        tyson_locations.update(get_location_names_with_ids(["Mike Tyson Decision"]))


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


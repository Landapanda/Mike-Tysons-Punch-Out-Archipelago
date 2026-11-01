from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import MTPOWorld

ITEM_NAME_TO_ID = {
    "Glass Joe": 1,
    "Von Kaiser": 2,
    "Piston Honda": 3,
    "Don Flamenco": 4,
    "King Hippo": 5,
    "Great Tiger": 6,
    "Bald Bull": 7,
    "Piston Honda 2": 8,
    "Soda Popinski": 9,
    "Bald Bull 2": 10,
    "Don Flamenco 2": 11, 
    "Mr. Sandman": 12,
    "Super Macho Man": 13,
    "Mike Tyson": 14,
    "Star Punch Unlock": 15,
    "Progressive Round": 16,
    "Heal in Between Rounds": 17,
    "Busy Signal Code": 18,
    "Credits Code": 19,
    "Filler": 20,
    "Math Trap": 21
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Glass Joe": ItemClassification.progression,
    "Von Kaiser": ItemClassification.progression,
    "Piston Honda": ItemClassification.progression,
    "Don Flamenco": ItemClassification.progression,
    "King Hippo": ItemClassification.progression,
    "Great Tiger": ItemClassification.progression,
    "Bald Bull": ItemClassification.progression,
    "Piston Honda 2": ItemClassification.progression,
    "Soda Popinski": ItemClassification.progression,
    "Bald Bull 2": ItemClassification.progression,
    "Don Flamenco 2": ItemClassification.progression,
    "Mr. Sandman": ItemClassification.progression,
    "Super Macho Man": ItemClassification.progression,
    "Mike Tyson": ItemClassification.progression,
    "Star Punch Unlock": ItemClassification.progression,
    "Progressive Round": ItemClassification.progression,
    "Heal in Between Round": ItemClassification.useful,
    "Busy Signal Code": ItemClassification.filler,
    "Credits Code": ItemClassification.filler,
    "Math Trap": ItemClassification.trap,
}

class MTPOItem(Item):
    game = "Mike Tyson's Punch-Out!!"


def get_random_filler_item_name(world: MTPOWorld) -> str:
    # APQuest has an option called "trap_chance".
    # This is the percentage chance that each filler item is a Math Trap instead of a Confetti Cannon.
    # For this purpose, we need to use a random generator.

    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    if world.random.randint(0, 99) < world.options.trap_chance:
        return "Math Trap"
    return "Filler"


def create_item_with_correct_classification(world: MTPOWorld, name: str) -> MTPOItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # It is perfectly normal and valid for an item's classification to differ based on the player's options.
    # In our case, Health Upgrades are only relevant to logic (and thus labeled as "progression") in hard mode.
    # if name == "Health Upgrade" and world.options.hard_mode:
    #     classification = ItemClassification.progression

    return MTPOItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: MTPOWorld) -> None:
    itempool: list[Item] = [
        world.create_item("Von Kaiser"),
        world.create_item("Piston Honda"),
        world.create_item("Don Flamenco"),
        world.create_item("King Hippo"),
        world.create_item("Great Tiger"),
        world.create_item("Bald Bull"),
        world.create_item("Piston Honda 2"),
        world.create_item("Soda Popinski"),
        world.create_item("Bald Bull 2"),
        world.create_item("Don Flamenco 2"),
        world.create_item("Mr. Sandman"),
        world.create_item("Super Macho Man"),
        world.create_item("Mike Tyson"),
        world.create_item("Star Punch Unlock"),
        world.create_item("Progressive Round"),
        world.create_item("Progressive Round"),
        world.create_item("Busy Signal Code"),
        world.create_item("Busy Signal Code"),
        world.create_item("Busy Signal Code"),
        world.create_item("Credits Code")
    ]

    starting_fighter = world.create_item("Glass Joe")
    world.push_precollected(starting_fighter)
    world.push_precollected(world.create_item("Progressive Round"))

    # Some items may only exist if the player enables certain options.
    # In our case, If the hammer option is enabled, the sixth item is the Hammer.
    # Otherwise, we add a filler Confetti Cannon.
    # if world.options.hammer:
        # Once again, it is important to stress that even though the Hammer doesn't always exist,
        # it must be present in the worlds item_name_to_id.
        # Whether it is actually in the itempool is determined purely by whether we create and add the item here.
        # itempool.append(world.create_item("Hammer"))

    # Archipelago requires that each world submits as many locations as it submits items.
    # This is where we can use our filler and trap items.
    # APQuest has two of these: The Confetti Cannon and the Math Trap.
    # (Unfortunately, Archipelago is a bit ambiguous about its terminology here:
    #  "filler" is an ItemClassification separate from "trap", but in a lot of its functions,
    #  Archipelago will use "filler" to just mean "an additional item created to fill out the itempool".
    #  "Filler" in this sense can technically have any ItemClassification,
    #  but most commonly ItemClassification.filler or ItemClassification.trap.
    #  Starting here, the word "filler" will be used to collectively refer to APQuest's Confetti Cannon and Math Trap,
    #  which are ItemClassification.filler and ItemClassification.trap respectively.)
    # Creating filler items works the same as any other item. But there is a question:
    # How many filler items do we actually need to create?
    # In regions.py, we created either six or seven locations depending on the "extra_starting_chest" option.
    # In this function, we have created five or six items depending on whether the "hammer" option is enabled.
    # We *could* have a really complicated if-else tree checking the options again, but there is a better way.
    # We can compare the size of our itempool so far to the number of locations in our world.

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as mtpo_options 
from .locations import LOCATION_NAME_TO_ID

class MTPOWorld(World):
    game = "Mike Tyson's Punch-Out!!"
    web = web_world.MTPOWebWorld()
    options_dataclass = mtpo_options.MTPOOptions
    options: mtpo_options.MTPOOptions
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    origin_region_name = "Joe"

    def create_regions(self) -> None:
        regions.create_all_regions(self)
        regions.connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.MTPOItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self):
        return {
            "goal": self.options.goal.value
        }
    
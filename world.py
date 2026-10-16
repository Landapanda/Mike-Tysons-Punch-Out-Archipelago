from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as apquest_options 

class MTPOWorld(World):
    def create_items(self) -> None:
        items.create_all_items(self)
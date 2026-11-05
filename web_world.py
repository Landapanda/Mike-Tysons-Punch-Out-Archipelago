from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class MTPOWebWorld(WebWorld):
    game = "Mike Tyson's Punch-Out!!"
    rich_text_options_doc = True
    option_groups = option_groups

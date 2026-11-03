from NetUtils import ClientStatus
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import logging
from .locations import LOCATION_NAME_TO_ID
from . import options, world

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

# RAM
CURRENT_MATCH = 0x001
CURRENT_OPPONENT_1 = 0x002
CURRENT_OPPONENT_2 = 0x003
FIGHT_IN = 0x004 # FF = in fight, 01 = Not in fight
KNOCKED_DOWN = 0x005
CURRENT_ROUND = 0x006
CURRENT_COUNT = 0x00C1
MINUTE = 0x0302
INIT_STAR = 0x0340
STARS_HELD = 0x0342
STARS_INC = 0x0343
STARS_HAVE = 0x34A # 64 + star amount (65 = 1 star)
OPPONENT_KNOCKDOWNS = 0x03CA
SELECT_REFILL = 0x03D9 #HP refilled in between rounds
SCORE_10000 = 0x03E9 #Ten-thousandths place
SCORE_1000 = 0x03EA # Thousandths place

# ROM
busy_signal_rom = [0x0EDAC, 0x0EDAD, 0x0EDAE, 0x0EDAF, 0x0EDB0, 0x0EDB1, 0x0EDB2, 0x0EDB3, 0x0EDB4, 0x0EDB5]
busy_signal_code = [8, 0, 0, 4, 2, 2, 2, 6, 0, 2]
busy_signal_2_rom = [0x0EDA2, 0x0EDA3, 0x0EDA4, 0x0EDA5, 0x0EDA6, 0x0EDA7, 0x0EDA8, 0x0EDA9, 0x0EDAA, 0xEDAB]
busy_signal_2_code = [0, 7, 5, 5, 4, 1, 6, 1, 1, 3]
busy_signal_3_rom = [0x0EDB6, 0x0EDB7, 0x0EDB8, 0x0EDB9, 0x0EDBA, 0x0EDBB, 0x0EDBC, 0x0EDBD, 0x0EDBE, 0x0EDBF]
busy_signal_3_code = [2, 0, 6, 8, 8, 2, 2, 0, 4, 0]
credits_rom = [0x0EDCA, 0x0EDCB, 0x0EDCC, 0x0EDCD, 0x0EDCE, 0x0EDCF, 0x0EDD0, 0x0EDD1, 0x0EDD2, 0x0EDD3]
credits_code = [1, 0, 6, 1, 1, 3, 0, 1, 2, 0]

IN_FIGHT = 255 #0xFF
OPPONENT_KNOCKED_DOWN = 1
TKO = 3
KO = 163 # A3 = 10 count
DECISION = 4 # After round 3 it becomes 4 for the decision

# (opponent_1, opponent_2)
JOE = (0, 0, 5)
KAISER = (2, 0)
HONDA_1 = (5, 48)
DON_1 = (0, 16)
HIPPO = (1, 00)
TIGER = (2, 16)
BULL_1 = (3, 48)
HONDA_2 = (5, 32)
SODA = (4, 16)
BULL_2 = (3, 32)
DON_2 = (0, 32)
SANDMAN = (3, 16)
MACHO = (4, 48)
TYSON = (5, 64)
DEMO = (3, 0)

goals = [32, 33, 34]

logger = logging.getLogger("Client")

class MTPOClient(BizHawkClient):
    game = "Mike Tyson's Punch-Out!!"
    system = "NES"
    patch_suffix = ".apmtpo"

    items: int = 0
    has_kaiser: bool = False
    has_honda_1: bool = False
    has_don_1: bool = False
    has_hippo: bool = False
    has_tiger: bool = False
    has_bull_1: bool = False
    has_honda_2: bool = False
    has_soda: bool = False
    has_bull_2: bool = False
    has_don_2: bool = False
    has_sandman: bool = False
    has_macho: bool = False
    has_tyson: bool = False

    stars_unlocked: bool = False
    rounds_unlocked: int = 1
    heal_unlocked: bool = False
    busy_1_unlocked: bool = False
    busy_2_unlocked: bool = False
    busy_3_unlocked: bool = False
    credits_unlocked: bool = False

    star_can_send: bool = False
    stars_received: int = 0
    stars_pending: int = 0
    previous_match: int = None
    star_queue_logged: bool = False

    def __init__(self):
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        rom_system = await bizhawk.get_system(ctx.bizhawk_ctx)
        
        from worlds._bizhawk import read, RequestFailedError
        try:
            rom_check = await read(ctx.bizhawk_ctx, [(0x0, 8, "PRG ROM")])
        except RequestFailedError:
            return False

        try:
            # Checks for first row of bytes. Could be changed to check for "TYSON" but would negate using Mr. Dream version
            if rom_system == "NES" and bytes(rom_check[0]) == bytes.fromhex("3080EF8A238BB692"):
                ctx.game = self.game
                ctx.items_handling = 0b111
                ctx.want_slot_data = True
                ctx.tags = {"AP"}
                ctx.set_notify("stars")
                logger.info("WORKING!!")
                return True
            else:
                return False
        except:
            return False

    async def on_package(self, ctx: "BizHawkClientContext", cmd, args):
       if cmd == "Retrieved":
        stars = ctx.stored_data.get("stars", 0)
        logger.info(f"Stars already sent: {stars}")


    def check_unlocks(self, ctx: "BizHawkClientContext") -> None:
        self.has_kaiser = False
        self.has_honda_1 = False
        self.has_don_1 = False
        self.has_hippo = False
        self.has_tiger = False
        self.has_bull_1 = False
        self.has_honda_2 = False
        self.has_soda = False
        self.has_bull_2 = False
        self.has_don_2 = False
        self.has_sandman = False
        self.has_macho = False
        self.has_tyson = False

        self.stars_unlocked = False
        self.rounds_unlocked = 0
        self.heal_unlocked = False
        self.busy_1_unlocked = False
        self.busy_2_unlocked = False
        self.busy_3_unlocked = False
        self.credits_unlocked = False
        
        self.stars_received = 0

        for item in ctx.items_received:
            name = ctx.item_names.lookup_in_game(item.item)
            if name == "Von Kaiser":
                self.has_kaiser = True
            if name == "Piston Honda":
                self.has_honda_1 = True
            if name == "Don Flamenco":
                self.has_don_1 = True
            if name == "King Hippo":
                self.has_hippo = True
            if name == "Great Tiger":
                self.has_tiger = True
            if name == "Bald Bull":
                self.has_bull_1 = True
            if name == "Piston Honda 2":
                self.has_honda_2 = True
            if name == "Soda Popinski":
                self.has_soda = True
            if name == "Bald Bull 2":
                self.has_bull_2 = True
            if name == "Don Flamenco 2":
                self.has_don_2 = True
            if name == "Mr. Sandman":
                self.has_sandman = True
            if name == "Super Macho Man":
                self.has_macho = True
            if name == "Mike Tyson":
                self.has_tyson = True
            if name == "Star Punch Unlock":
                self.stars_unlocked = True
            if name == "Progressive Round":
                self.rounds_unlocked += 1
            if name == "Heal in Between Rounds":
                self.heal_unlocked = True
            if name == "Busy Signal Code":
                self.busy_1_unlocked = True
            if name == "Busy Signal Code 2":
                self.busy_2_unlocked = True
            if name == "Busy Signal Code 3":
                self.busy_3_unlocked = True
            if name == "Credits Code":
                self.credits_unlocked = True
            if name == "Star":
                self.stars_received += 1
        self.stars_pending = self.stars_received - ctx.stored_data.get("stars", 0)
                

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write
        if ctx.server is None or ctx.auth is None:
            return

        reads = await read(ctx.bizhawk_ctx, [
            (CURRENT_MATCH, 1, "RAM"),
            (CURRENT_OPPONENT_1, 1, "RAM"),
            (CURRENT_OPPONENT_2, 1, "RAM"),
            (KNOCKED_DOWN, 1, "RAM"),
            (CURRENT_ROUND, 1, "RAM"),
            (OPPONENT_KNOCKDOWNS, 1, "RAM"),
            (CURRENT_COUNT, 1, "RAM"),
            (MINUTE, 1, "RAM"),
            (FIGHT_IN, 1, "RAM"),
            (STARS_HELD, 1, "RAM"),
            (INIT_STAR, 1, "RAM"),
            (STARS_INC, 1, "RAM"),
            (STARS_HAVE, 1, "RAM"),
            (SCORE_1000, 1, "RAM"),
            (SCORE_10000, 1, "RAM"),
            (SELECT_REFILL, 1, "RAM")
        ])
        (match, opponent_1, opponent_2, knockdown, round, opponent_knockdown_count, 
         down_count, timer_minute, fight_status, stars, star_able, inc_stars, star_has, score_thousand, score_ten_thousand,
         hp_refill) = (r[0] for r in reads)
        writes = []

        # logger.info(
        # f"Match={match}, Opponent1={opponent_1}, "
        # f"Opponent2={opponent_2}, "
        # f"Knockdown={knockdown}, KDCount={opponent_knockdown_count},"
        # f"Count={down_count}, Fight={fight_status},"
        # )

        # Location Checks
        if fight_status == IN_FIGHT:
            #Glass Joe
            location_id = None
            if opponent_1 == JOE[0] and opponent_2 == JOE[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[0]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[1]
                elif round == DECISION and score_thousand >= 5:
                    location_id = list(LOCATION_NAME_TO_ID.values())[2]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])
                
            #Von Kaiser
            location_id = None
            if opponent_1 == KAISER[0] and opponent_2 == KAISER[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[3]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[4]
                elif round == DECISION and score_thousand >= 8:
                    location_id = list(LOCATION_NAME_TO_ID.values())[5]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Piston Honda 1
            location_id = None
            if opponent_1 == HONDA_1[0] and opponent_2 == HONDA_1[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[6]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[7]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Don Flamenco 1
            location_id = None
            if opponent_1 == DON_1[0] and opponent_2 == DON_1[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[8]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[9]
                elif round == DECISION and score_ten_thousand >= 1:
                    location_id = list(LOCATION_NAME_TO_ID.values())[10]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            # King Hippo
            location_id = None
            if opponent_1 == HIPPO[0] and opponent_2 == HIPPO[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[11]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Great Tiger
            location_id = None
            if opponent_1 == TIGER[0] and opponent_2 == TIGER[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[12]
                elif round == DECISION and score_ten_thousand >= 1:
                    location_id = list(LOCATION_NAME_TO_ID.values())[13]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Bald Bull
            location_id = None
            if opponent_1 == BULL_1[0] and opponent_2 == BULL_1[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[14]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Piston Honda 2
            location_id = None
            if opponent_1 == HONDA_2[0] and opponent_2 == HONDA_2[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[15]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[16]
                elif round == DECISION and score_thousand >= 5:
                    location_id = list(LOCATION_NAME_TO_ID.values())[17]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Soda Popinski
            location_id = None
            if opponent_1 == SODA[0] and opponent_2 == SODA[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[18]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[19]
                elif round == DECISION and score_ten_thousand >= 1:
                    location_id = list(LOCATION_NAME_TO_ID.values())[20]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Bald Bull 2
            location_id = None
            if opponent_1 == BULL_2[0] and opponent_2 == BULL_2[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[21]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[22]
                elif round == DECISION and score_thousand >= 7:
                    location_id = list(LOCATION_NAME_TO_ID.values())[23]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]) 

            #Don Flamenco 2
            location_id = None
            if opponent_1 == DON_2[0] and opponent_2 == DON_2[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[24]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[25]
                elif round == DECISION and score_ten_thousand >= 5:
                    location_id = list(LOCATION_NAME_TO_ID.values())[26]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]) 

            #Mr. Sandman
            location_id = None
            if opponent_1 == SANDMAN[0] and opponent_2 == SANDMAN[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[27]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[28]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Super Macho Man
            location_id = None
            if opponent_1 == MACHO[0] and opponent_2 == MACHO[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[29]
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[30]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Mike Tyson
            location_id = None
            if opponent_1 == TYSON[0] and opponent_2 == TYSON[1]:
                if knockdown == OPPONENT_KNOCKED_DOWN and opponent_knockdown_count == TKO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[31]
                    if not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                elif knockdown == OPPONENT_KNOCKED_DOWN and down_count == KO:
                    location_id = list(LOCATION_NAME_TO_ID.values())[32]
                elif round == DECISION and score_thousand >= 5:
                    location_id = list(LOCATION_NAME_TO_ID.values())[33]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])
                    if location_id == goals.values()[ctx.slot_data["goal"]] and not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        # Item Checks
        if not match == 19: # Hopefully prevents visual glitch on the Bull DEMO fight that can sometimes freeze the game.
            if not self.has_kaiser:
                if match >= 1:
                    writes.extend([
                        (CURRENT_MATCH, bytes([0]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([JOE[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([JOE[1]]), "RAM")
                    ])
            elif not self.has_honda_1:
                if match >= 2:
                    writes.extend([
                        (CURRENT_MATCH, bytes([1]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([KAISER[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([KAISER[1]]), "RAM")
                    ])
            elif not self.has_don_1:
                if match >= 3:
                    writes.extend([
                        (CURRENT_MATCH, bytes([2]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([HONDA_1[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([HONDA_1[1]]), "RAM")
                    ])
            elif not self.has_hippo:
                if match >= 4:
                    writes.extend([
                        (CURRENT_MATCH, bytes([3]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([DON_1[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([DON_1[1]]), "RAM")
                    ])
            elif not self.has_tiger:
                if match >= 5:
                    writes.extend([
                        (CURRENT_MATCH, bytes([4]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([HIPPO[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([HIPPO[1]]), "RAM")
                    ])
            elif not self.has_bull_1:
                if match >=6:
                    writes.extend([
                        (CURRENT_MATCH, bytes([5]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([TIGER[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([TIGER[1]]), "RAM")
                    ])
            elif not self.has_honda_2:
                if match >= 7:
                    writes.extend([
                        (CURRENT_MATCH, bytes([6]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([TIGER[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([TIGER[1]]), "RAM")
                    ])
            elif not self.has_soda:
                if match >= 8:
                    writes.extend([
                        (CURRENT_MATCH, bytes([7]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([HONDA_2[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([HONDA_2[1]]), "RAM")
                    ])
            elif not self.has_bull_2:
                if match >= 9:
                    writes.extend([
                        (CURRENT_MATCH, bytes([8]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([SODA[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([SODA[1]]), "RAM")
                    ])
            elif not self.has_don_2:
                if match >= 10:
                    writes.extend([
                        (CURRENT_MATCH, bytes([9]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([BULL_2[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([BULL_2[1]]), "RAM")
                    ])
            if not self.has_sandman:
                if match >= 11:
                    writes.extend([
                        (CURRENT_MATCH, bytes([10]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([DON_2[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([DON_2[1]]), "RAM")
                    ])
            elif not self.has_macho:
                if match >= 12:
                    writes.extend([
                        (CURRENT_MATCH, bytes([11]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([SANDMAN[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([SANDMAN[1]]), "RAM")
                    ])
            elif not self.has_tyson:
                if match >= 13:
                    writes.extend([
                        (CURRENT_MATCH, bytes([12]), "RAM"),
                        (CURRENT_OPPONENT_1, bytes([MACHO[0]]), "RAM"), 
                        (CURRENT_OPPONENT_2, bytes([MACHO[1]]), "RAM")
                    ])
        if not self.stars_unlocked:
            writes.extend([
                (INIT_STAR, bytes([0]), "RAM"),
                (STARS_INC, bytes([0]), "RAM"),
                (STARS_HAVE, bytes([64]), "RAM")
            ])
        if self.rounds_unlocked == 1 and round == 1 and timer_minute == 3 and fight_status == IN_FIGHT:
            writes.extend([
                (CURRENT_ROUND, bytes([3]), "RAM"),
                (SCORE_10000, bytes([0]), "RAM"),
                (SCORE_1000, bytes([0]), "RAM")
            ])
        if self.rounds_unlocked == 2 and round == 2 and timer_minute == 3 and fight_status == IN_FIGHT:
            writes.extend([
                (CURRENT_ROUND, bytes([3]), "RAM"),
                (SCORE_10000, bytes([0]), "RAM"),
                (SCORE_1000, bytes([0]), "RAM")
            ])
        if not self.heal_unlocked:
            writes.append(
                (SELECT_REFILL, bytes([0]), "RAM")
            )
        if not self.busy_1_unlocked:
            for i in busy_signal_rom:
                writes.append(
                    (i, bytes([255]), "PRG ROM")
                )
        else:
            for i in range(len(busy_signal_rom)):
                writes.append(
                    (busy_signal_rom[i], bytes([busy_signal_code[i]]), "PRG ROM")
                )
        if not self.busy_2_unlocked:
            for i in busy_signal_2_rom:
                writes.append(
                    (i, bytes([255]), "PRG ROM")
                )
        else:
            for i in range(len(busy_signal_2_rom)):
                writes.append(
                    (busy_signal_rom[i], bytes([busy_signal_2_code[i]]), "PRG ROM")
                )
        if not self.busy_3_unlocked:
            for i in busy_signal_3_rom:
                writes.append(
                    (i, bytes([255]), "PRG ROM")
                )
        else:
            for i in range(len(busy_signal_3_rom)):
                writes.append(
                    (busy_signal_rom[i], bytes([busy_signal_3_code[i]]), "PRG ROM")
                )
        if not self.credits_unlocked:
            for i in credits_rom:
                writes.append(
                    (i, bytes([255]), "PRG ROM")
                )
        else:
            for i in range(len(credits_rom)):
                writes.append(
                    (credits_rom[i], bytes([credits_code[i]]), "PRG ROM")
                )
        if self.stars_unlocked and self.stars_pending > 0:
            # Check for match changing. Could be updated to include losses.
            if self.previous_match is None:
                self.previous_match = match
            elif match != self.previous_match:
                if match != 19 and self.previous_match != 19:
                    self.star_can_send = True
                self.previous_match = match
            stars_sending = min(3, self.stars_pending)
            if not self.star_queue_logged:
                logger.info(f"{self.stars_pending} Star(s) queued for next fight!")
                self.star_queue_logged = True
            if self.star_can_send and fight_status == IN_FIGHT:
                star_add = [
                    (STARS_HELD, bytes([stars + stars_sending]), "RAM"),
                    (STARS_HAVE, bytes([star_has + stars_sending]), "RAM"),
                ]
                await write(ctx.bizhawk_ctx, star_add)
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": "stars",
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "add", "value": stars_sending}]
                }])
                self.stars_pending -= stars_sending
                self.star_can_send = False
                # logger.info(
                # f"{self.previous_match}, {match}\ncan_send={self.star_can_send}\n"
                # f"stars: {self.stars_pending}, data:{ctx.stored_data.get("stars", 0)}"
                # )
                logger.info(f"{stars_sending} star(s) sent!")
        else:
            self.star_queue_logged = False
            
        
        # Check Unlocks
        self.check_unlocks(ctx)
        if self.items < len(ctx.items_received):
            item = ctx.items_received[self.items]
            item_name = ctx.item_names.lookup_in_game(item.item)

            if item_name == "Von Kaiser":
                self.items += 1
            elif item_name == "Piston Honda":
                self.items += 1
            elif item_name == "Don Flamenco":
                self.items += 1
            elif item_name == "King Hippo":
                self.items += 1
            elif item_name == "Great Tiger":
                self.items += 1
            elif item_name == "Bald Bull":
                self.items += 1
            elif item_name == "Piston Honda 2":
                self.items += 1
            elif item_name == "Soda Popinski":
                self.items += 1
            elif item_name == "Bald Bull 2":
                self.items += 1
            elif item_name == "Don Flamenco 2":
                self.items += 1
            elif item_name == "Mr. Sandman":
                self.items += 1
            elif item_name == "Super Macho Man":
                self.items += 1
            elif item_name == "Mike Tyson":
                self.items += 1
            elif item_name == "Star Punch Unlock":
                self.items += 1
            elif item_name == "Progressive Round":
                self.items += 1
            elif item_name == "Heal in Between Rounds":
                self.items += 1
            elif item_name == "Busy Signal Code":
                self.items += 1
            elif item_name == "Credits Code":
                self.items += 1
            elif item_name == "End Round Trap":
                self.items += 1
            elif item_name == "Star":
                 self.items += 1

        if writes:
            await write(ctx.bizhawk_ctx, writes)
        
        
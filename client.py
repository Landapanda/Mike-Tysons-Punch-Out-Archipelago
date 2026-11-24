from NetUtils import ClientStatus
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import logging
from .locations import get_location_names_with_ids

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

# RAM
CURRENT_MATCH = 0x001
CURRENT_OPPONENT_1 = 0x002
CURRENT_OPPONENT_2 = 0x003
FIGHT_IN = 0x004 # FF = in fight, 01 = Not in fight
KNOCKED_DOWN = 0x005
CURRENT_ROUND = 0x006
CURRENT_COUNT = 0x00C1
LOSSES = 0x0173
MINUTE = 0x0302
SECONDS_10 = 0x304
SECONDS_01 = 0x305
INIT_STAR = 0x0340
STARS_HELD = 0x0342
STARS_INC = 0x0343
STARS_HAVE = 0x34A # 64 + star amount (65 = 1 star)
OPPONENT_KNOCKDOWNS = 0x03CA
SELECT_REFILL = 0x03D9 #HP refilled in between rounds
SCORE_10000 = 0x03E9 #Ten-thousandths place
SCORE_1000 = 0x03EA # Thousandths place

# ROM
busy_signal_rom = []
busy_signal_2_rom = []
busy_signal_3_rom = []
credits_rom = []
for i in range(0x0EDAC, 0x0EDB5+1):
    busy_signal_rom.append(i)
for i in range(0x0EDA2, 0xEDAB+1):
    busy_signal_2_rom.append(i)
for i in range(0x0EDB6, 0x0EDBF+1):
    busy_signal_3_rom.append(i)
for i in range(0x0EDCA, 0x0EDD3+1):
    credits_rom.append(i)
busy_signal_code = [8, 0, 0, 4, 2, 2, 2, 6, 0, 2]
busy_signal_2_code = [0, 7, 5, 5, 4, 1, 6, 1, 1, 3]
busy_signal_3_code = [2, 0, 6, 8, 8, 2, 2, 0, 4, 0]
credits_code = [1, 0, 6, 1, 1, 3, 0, 1, 2, 0]

# kaiser_kd4 = []
# for i in range(0x0532D, 0x05333+1):
#     kaiser_kd4.append(i)
# honda_kd4 = []
# for i in range(0x0BC4F, 0x0BC55+1):
#     honda_kd4.append(i)
# soda_kd5 = []
# for i in range():
#     soda_kd5.append(i)
sandman_kd6 = []
for i in range(0x07DB2, 0x7DB8+1):
    sandman_kd6.append(i)

tiger_hp_kd = {
    "kd3": [],
    "kd4": [],
    "kd5": [],
    "kd6": []
} 

bull_hp_kd = {
    "kd3": [],
    "kd4": [],
    "kd5": [],
    "kd6": []
} 

for i in range(0x0548C, 0x05492+1):
    tiger_hp_kd["kd3"].append(i)
for i in range(0x05494, 0x0549A+1):
    tiger_hp_kd["kd4"].append(i)
for i in range(0x0549C, 0x054A2+1):
    tiger_hp_kd["kd5"].append(i)
for i in range(0x054A4, 0x054AA+1):
    tiger_hp_kd["kd6"].append(i)

for i in range(0x07A10, 0x07A16+1):
    bull_hp_kd["kd3"].append(i)
for i in range(0x07A18, 0x07A1E+1):
    bull_hp_kd["kd4"].append(i)
for i in range(0x07A20, 0x07A26+1):
    bull_hp_kd["kd5"].append(i)
for i in range(0x07A28, 0x07A2E+1):
    bull_hp_kd["kd6"].append(i)



IN_FIGHT = 255 #0xFF
OPPONENT_KNOCKED_DOWN = 1
TKO = 3
KO = 163 # A3 = 10 count
DECISION = 4 # After round 3 it becomes 4 for the decision

# (opponent_1, opponent_2, score_req (in thousands))
JOE = (0, 0, 5)
KAISER = (2, 0, 8)
HONDA_1 = (5, 48, None)
DON_1 = (0, 16, 10)
HIPPO = (1, 00, None)
TIGER = (2, 16, 10)
BULL_1 = (3, 48, None)
HONDA_2 = (5, 32, 3)
SODA = (4, 16, 10)
BULL_2 = (3, 32, 7)
DON_2 = (0, 32, 5)
SANDMAN = (3, 16, None)
MACHO = (4, 48, None)
TYSON = (5, 64, 5)
DEMO = (3, 0, None)

goal_ids = [
    list(get_location_names_with_ids(["Defeat Super Macho Man"]).values())[0], 
    list(get_location_names_with_ids(["KO Super Macho Man"]).values())[0],
    list(get_location_names_with_ids(["Super Macho Man Decision"]))[0],
    list(get_location_names_with_ids(["Defeat Mike Tyson"]).values())[0], 
    list(get_location_names_with_ids(["KO Mike Tyson"]).values())[0], 
    list(get_location_names_with_ids(["Mike Tyson Decision"]).values())[0]
]

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

    # fighters_unlocked: list = [0]

    stars_unlocked: bool = False
    rounds_unlocked: int = 1
    heal_unlocked: bool = False
    busy_1_unlocked: bool = False
    busy_2_unlocked: bool = False
    busy_3_unlocked: bool = False
    credits_unlocked: bool = False

    previous_match: int = None
    match_changed: bool = False
    previous_round: int = None
    round_changed: bool = False
    previous_losses: int = None
    losses_changed: bool = False

    stars_received: int = 0
    stars_pending: int = 0
    star_can_send: bool = False
    star_queue_logged: bool = False

    end_round_trap_received: int = 0
    end_round_trap_pending: int = 0
    trap_can_send: bool = False
    trap_queue_logged: bool = False

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
                ctx.set_notify("end_rounds")
                return True
            else:
                return False
        except:
            return False

    async def on_package(self, ctx: "BizHawkClientContext", cmd, args):
       if cmd == "Retrieved":
        stars = ctx.stored_data.get("stars", 0)
        end_rounds = ctx.stored_data.get("end_rounds", 0)


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
        stored_stars = ctx.stored_data.get("stars") or 0
        self.end_round_trap_received = 0
        stored_end_rounds = ctx.stored_data.get("end_rounds") or 0

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
            if name == "End Round Trap":
                self.end_round_trap_received += 1
        self.stars_pending = self.stars_received - stored_stars
        self.end_round_trap_pending = self.end_round_trap_received - stored_end_rounds
                

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk import read, write
        if ctx.server is None or ctx.auth is None:
            return

        goal = ctx.slot_data["goal"]
        decision_on: bool = ctx.slot_data["decision"]
        force_ko: bool = ctx.slot_data["force_ko"]
        add_ko: bool = ctx.slot_data["add_ko"]
        if add_ko:
            tiger_ko_con = ctx.slot_data["tiger_ko"]
            bull_ko_con = ctx.slot_data["bull_ko"]
        add_decision: bool = ctx.slot_data["add_decision"]
        if decision_on and add_decision:
            honda_req = ctx.slot_data["honda_decision"]
            bull_req = ctx.slot_data["bull_decision"]
            sandman_req = ctx.slot_data["sandman_decision"]
        if (add_decision or goal == 2) or (add_decision and goal not in [0, 1]):
            macho_req = ctx.slot_data["macho_decision"] 

        reads = await read(ctx.bizhawk_ctx, [
            (CURRENT_MATCH, 1, "RAM"),
            (CURRENT_OPPONENT_1, 1, "RAM"),
            (CURRENT_OPPONENT_2, 1, "RAM"),
            (KNOCKED_DOWN, 1, "RAM"),
            (CURRENT_ROUND, 1, "RAM"),
            (OPPONENT_KNOCKDOWNS, 1, "RAM"),
            (CURRENT_COUNT, 1, "RAM"),
            (LOSSES, 1, "RAM"),
            (MINUTE, 1, "RAM"),
            (SECONDS_10, 1, "RAM"),
            (SECONDS_01, 1, "RAM"),
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
         down_count, losing, timer_minute, timer_second_10, timer_second_01, fight_status, stars, star_able, 
         inc_stars, star_has, score_thousand, score_ten_thousand, hp_refill) = (r[0] for r in reads)
        writes = []

        tko_logic = (knockdown == OPPONENT_KNOCKED_DOWN) and (opponent_knockdown_count == TKO)
        ko_logic = (knockdown == OPPONENT_KNOCKED_DOWN) and (down_count == KO)

        def decision_logic_maker(fighter):
            if fighter is not list:
                score_req = fighter
            else:
                score_req = fighter[2]
            if score_req == 10:
                scoring = score_ten_thousand
                score_req = 1
            else:
                scoring = score_thousand
            decision_logic = (round == DECISION) and (scoring >= score_req)
            return decision_logic

        def add_decision_maker(rom, req):
            if req == 10:
                writes.append(
                    (rom[2], bytes([req]), "PRG ROM")
                )
            else:
                writes.extend([
                    (rom[2], bytes([0]), "PRG ROM"),
                    (rom[3], bytes([req]), "PRG ROM")
                ])


        if force_ko:
            for i in sandman_kd6:
                writes.append(
                    (i, bytes([0]), "PRG ROM")
                )

        if add_ko:
            if tiger_ko_con == 3:
                for i in tiger_hp_kd["kd3"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            elif tiger_ko_con == 4:
                for i in tiger_hp_kd["kd4"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            elif tiger_ko_con == 5:
                for i in tiger_hp_kd["kd5"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            else:
                for i in tiger_hp_kd["kd6"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            if bull_ko_con == 3:
                for i in bull_hp_kd["kd3"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            elif bull_ko_con == 4:
                for i in bull_hp_kd["kd4"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            elif bull_ko_con == 5:
                for i in bull_hp_kd["kd5"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
            else:
                for i in bull_hp_kd["kd6"]:
                    writes.append(
                        (i, bytes([0]), "PRG ROM")
                    )
        # Add Decision
        if decision_on and add_decision:
            honda_decision_rom = [0x0BB60, 0x0BB61, 0x0BB62, 0x0BB63] # (1000k?, 100k, 10k, 1k)
            bull_decision_rom = [0x078FF, 0x07900, 0x07901, 0x07902]
            sandman_decision_rom = [0x07D1D, 0x07D1E, 0x07D1F, 0x07D20]
            writes.extend([
                (honda_decision_rom[0], bytes([0]), "PRG ROM"),
                (honda_decision_rom[1], bytes([0]), "PRG ROM"),
                (bull_decision_rom[0], bytes([0]), "PRG ROM"),
                (bull_decision_rom[1], bytes([0]), "PRG ROM"),
                (sandman_decision_rom[0], bytes([0]), "PRG ROM"),
                (sandman_decision_rom[1], bytes([0]), "PRG ROM"),
            ])
            add_decision_maker(honda_decision_rom, honda_req)
            add_decision_maker(bull_decision_rom, bull_req)
            add_decision_maker(sandman_decision_rom, sandman_req)
        if (add_decision or goal == 2) or (add_decision and goal not in [0, 1]):
            macho_decision_rom = [0x098A0, 0x098A1, 0x098A2, 0x098A3] 
            writes.extend([
                (macho_decision_rom[0], bytes([0]), "PRG ROM"),
                (macho_decision_rom[1], bytes([0]), "PRG ROM"),
            ])
            add_decision_maker(macho_decision_rom, macho_req)
        # Location Checks
        if fight_status == IN_FIGHT:
            #Glass Joe
            location_id = None
            location_name = None
            if opponent_1 == JOE[0] and opponent_2 == JOE[1]:
                if tko_logic:
                    location_name = "TKO Glass Joe"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Glass Joe"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(JOE):
                        location_name = "Glass Joe Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])
                
            #Von Kaiser
            location_id = None
            location_name = None
            if opponent_1 == KAISER[0] and opponent_2 == KAISER[1]:
                if tko_logic:
                    location_name = "TKO Von Kaiser"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Von Kaiser"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(KAISER):
                        location_name = "Von Kaiser Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Piston Honda 1
            location_id = None
            location_name = None
            if opponent_1 == HONDA_1[0] and opponent_2 == HONDA_1[1]:
                if tko_logic:
                    location_name = "TKO Piston Honda"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Piston Honda"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on and add_decision:
                    if decision_logic_maker(honda_req):
                        location_name = "Piston Honda Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Don Flamenco 1
            location_id = None
            location_name = None
            if opponent_1 == DON_1[0] and opponent_2 == DON_1[1]:
                if tko_logic:
                    location_name = "TKO Don Flamenco"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Don Flamenco"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(DON_1):
                        location_name = "Don Flamenco Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            # King Hippo
            location_id = None
            location_name = None
            if opponent_1 == HIPPO[0] and opponent_2 == HIPPO[1]:
                if ko_logic:
                    location_name = "KO King Hippo"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Great Tiger
            location_id = None
            location_name = None
            if opponent_1 == TIGER[0] and opponent_2 == TIGER[1]:
                if tko_logic:
                    location_name = "TKO Great Tiger"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if add_ko:
                    if ko_logic:
                        location_name = "KO Great Tiger"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(TIGER):
                        location_name = "Great Tiger Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Bald Bull
            location_id = None
            location_name = None
            if opponent_1 == BULL_1[0] and opponent_2 == BULL_1[1]:
                if tko_logic:
                    location_name = "TKO Bald Bull"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if add_ko:
                    if ko_logic:
                        location_name = "KO Bald Bull"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on and add_decision:
                    if decision_logic_maker(bull_req):
                        location_name = "Bald Bull Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Piston Honda 2
            location_id = None
            location_name = None
            if opponent_1 == HONDA_2[0] and opponent_2 == HONDA_2[1]:
                if tko_logic:
                    location_name = "TKO Piston Honda 2"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Piston Honda 2"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(HONDA_2):
                        location_name = "Piston Honda 2 Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Soda Popinski
            location_id = None
            location_name = None
            if opponent_1 == SODA[0] and opponent_2 == SODA[1]:
                if tko_logic:
                    location_name = "TKO Soda Popinski"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Soda Popinski"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(SODA):
                        location_name = "Soda Popinski Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

            #Bald Bull 2
            location_id = None
            location_name = None
            if opponent_1 == BULL_2[0] and opponent_2 == BULL_2[1]:
                if tko_logic:
                    location_name = "TKO Bald Bull 2"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Bald Bull 2"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(BULL_2):
                        location_name = "Bald Bull 2 Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]) 

            #Don Flamenco 2
            location_id = None
            location_name = None
            if opponent_1 == DON_2[0] and opponent_2 == DON_2[1]:
                if tko_logic:
                    location_name = "TKO Don Flamenco 2"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Don Flamenco 2"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on:
                    if decision_logic_maker(DON_2):
                        location_name = "Don Flamenco 2 Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])  

            #Mr. Sandman
            location_id = None
            location_name = None
            if opponent_1 == SANDMAN[0] and opponent_2 == SANDMAN[1]:
                if tko_logic:
                    location_name = "TKO Mr. Sandman"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif ko_logic:
                    location_name = "KO Mr. Sandman"
                    location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if decision_on and add_decision:
                    if decision_logic_maker(sandman_req):
                        location_name = "Mr. Sandman Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]) 
            
            #Super Macho Man
            location_id = None
            location_name = None
            if opponent_1 == MACHO[0] and opponent_2 == MACHO[1]:
                if goal > 2:
                    if tko_logic:
                        location_name = "TKO Super Macho Man"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                    elif ko_logic:
                        location_name = "KO Super Macho Man"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                    if decision_on and add_decision:
                        if decision_logic_maker(macho_req):
                            location_name = "Super Macho Man Decision"
                            location_id = list(get_location_names_with_ids([location_name]).values())[0]
                else:
                    if goal == 0:
                        if tko_logic or ko_logic or (decision_on and add_decision and decision_logic_maker(macho_req)):
                            location_name = "Defeat Super Macho Man"
                            location_id = list(get_location_names_with_ids([location_name]).values())[0]
                    elif goal == 1:
                        if ko_logic:
                            location_name = "KO Super Macho Man"
                            location_id = list(get_location_names_with_ids([location_name]).values())[0]
                    elif goal == 2:
                        if decision_logic_maker(macho_req):
                            location_name = "Super Macho Man Decision"
                            location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]) 
                if goal <= 2:
                    if location_id == goal_ids[goal] and not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

            #Mike Tyson
            location_id = None
            location_name = None
            if opponent_1 == TYSON[0] and opponent_2 == TYSON[1]:
                if goal == 3:
                    if tko_logic or ko_logic or (decision_logic_maker(TYSON)):
                        location_name = "Defeat Mike Tyson"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif goal == 4:
                    if ko_logic:
                        location_name = "KO Mike Tyson"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                elif goal == 5:
                    if decision_logic_maker(TYSON):
                        location_name = "Mike Tyson Decision"
                        location_id = list(get_location_names_with_ids([location_name]).values())[0]
                if location_id is not None and location_id not in ctx.checked_locations:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]) 
                    if not ctx.finished_game:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

        # Item Checks
        if not match == 19: # Hopefully prevents visual glitch on the Bull DEMO fight that can sometimes freeze the game.
            # ALT METHOD to allow skipping ahead by skipping to next fight rather than locking linearlly.
            #   Can't figure out right now saving for next update.
            # if match > max(self.fighters_unlocked):
            #     proper_match = max(self.fighters_unlocked)
            #     if proper_match in self.fighters_unlocked:
            #         writes.append(
            #             (CURRENT_MATCH, bytes([proper_match]), "RAM")
            #         )
            #     logger.info(f"Set fight to {proper_match}")
            #     logger.info(sorted(self.fighters_unlocked))
            # elif match not in self.fighters_unlocked:
            #     fighters = sorted(self.fighters_unlocked)
            #     proper_match = match+1
            #     logger.info(f"NOT IN LIST: {proper_match}")
            #     while proper_match not in self.fighters_unlocked:
            #         proper_match = match+1
            #         logger.info(f"NOT IN LIST: {proper_match}")
            #     else:
            #         writes.append(
            #             (CURRENT_MATCH, bytes([proper_match]), "RAM")
            #         )
                # if proper_match in self.fighters_unlocked:
                #     writes.append(
                #         (CURRENT_MATCH, bytes([proper_match]), "RAM")
                #     )
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
            self.star_can_send = False
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

        # Check for match/round/loss changing.
        if self.previous_match is None:
            self.previous_match = match
            self.match_changed = False
        elif match > self.previous_match:
            if match != 19 and self.previous_match != 19:
                self.match_changed = True
            else:
                self.match_changed = False
        self.previous_match = match

        if self.previous_round is None:
            self.previous_round = round
            self.round_changed = False
        elif round > self.previous_round:
            if (self.previous_round == 3 and round == 4) or match == 19 or round == 0:
                self.round_changed = False
            elif round != 4 and self.previous_round != 3 and round != 0 and match != 19:
                self.round_changed = True

        self.previous_round = round

        if self.previous_losses is None:
            self.previous_losses = losing
            self.losses_changed = False
        elif losing != self.previous_losses:
            if losing != 0:
                self.losses_changed = True
            else:
                self.losses_changed = False
        self.previous_losses = losing

        if not self.end_round_trap_pending >= 1:
            if not self.stars_unlocked or not self.stars_pending >= 1:
                self.previous_match = None
                self.previous_round = None
                self.previous_losses = None
        
        if self.stars_unlocked and self.stars_pending > 0: 
            if self.match_changed or self.round_changed or self.losses_changed:
                self.star_can_send = True
            else:
                self.star_can_send = False
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
                self.previous_match = None
                self.previous_round = None
                self.previous_losses = None
                logger.info(f"{stars_sending} star(s) sent!")
        else:
            self.star_queue_logged = False
       
        if self.end_round_trap_pending > 0:
            if self.match_changed or self.round_changed or self.losses_changed:
                self.trap_can_send = True
            else:
                self.trap_can_send = False
            if not self.trap_queue_logged:
                logger.info("Round End Trap queued.")
                self.trap_queue_logged = True
            if self.trap_can_send and fight_status == IN_FIGHT:
                skip_round = [
                    (MINUTE, bytes([2]), "RAM"),
                    (SECONDS_10, bytes([5]), "RAM"),
                    (SECONDS_01, bytes([9]), "RAM")
                    ]
                await write(ctx.bizhawk_ctx, skip_round)
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": "end_rounds",
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "add", "value": 1}]
                }])
                self.end_round_trap_pending -= 1
                self.trap_can_send = False
                self.previous_match = None
                self.previous_round = None
                self.previous_losses = None
                logger.info("Round End Trap sent.")
        else:
            self.trap_queue_logged = False
        
        # Check Unlocks
        self.check_unlocks(ctx)
        if self.items < len(ctx.items_received):
            item = ctx.items_received[self.items]
            item_name = ctx.item_names.lookup_in_game(item.item)
         
            if item_name is not None:
                self.items += 1

        if writes:
            await write(ctx.bizhawk_ctx, writes)
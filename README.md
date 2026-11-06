# Mike Tyson's Punch-Out!! Archipelago Randomizer
An Archipelago Randomizer for Mike Tyson's Punch-Out!! on NES.

## Checks
- TKOs: TKO all fighters by knocking them down 3 times in a single round.
- KOs: KO all fighters, if applicable, by meeting any of their knockout conditions. Most will require more than one round unlocked.
- Decisions:  Defeat all fighters by decision, where applicable, by earning their score requirement and surviving all three rounds. (Optional)

## Items
- Fighters: Starting with Glass Joe, you unlock every fighter individually.
- Progressive Rounds: Starting with a single round, unlock more rounds to gain access to KOs and Decisions.
- Star Punch Unlock: Start without the ability to earn stars and unlock the ability to earn and use stars.
- Healing: Unlock in between round healing.
- Stars: Obtain a free star at the start of the next fight.
- Pass Codes: Obtain Filler pass codes - Busy Signal Codes and the Credits Code
- Traps: End Round Trap, Go Pink Trap, -1000 Points Trap. (Only End Round Trap implemented so far, other two are just ideas for now.)

## Goals
- Defeat Super Macho Man: For those who aren't quite able to beat Mike Tyson. Defeat him by TKO or KO.
- KO Super Macho Man: Defeat Super Macho Man by KO.
- Defeat Mike Tyson: Defeat the final boss of the game Mike Tyson via TKO, KO, or Decision.
- KO Mike Tyson: Go for the extra challenge and make Tyson stay down for the 10-count.
- Mike Tyson Decision: Survive all three rounds and beat Mike Tyson via decision.

## Options
- Goal: Select your goal from the three options seen above.
- Decision Checks: Enable checks for decision wins.
- Force KO: Makes the RNG KO for Mr. Sandman a guaranteed KO. (Could be added to other fights but Sandman is the only complete RNG one.)
- Add KOs: Add KOs to Great Tiger and Bald Bull 1, select how many knockdowns to trigger their KOs.
- Trap Chance: Choose the percent of Filler items that become Traps.

## Notes
I am very new to AP as a whole and especially so with developing one, as well as developing in general. The best I can do is to try my best and make this as good as I can. However, I am open to any and all feedback or assistance! Feedback can be for ideas on checks, items, options, or logic.

## Resources
Huge thanks to these resources for me to even begin working on this project!
- [APQuest](https://github.com/ArchipelagoMW/Archipelago/tree/main/worlds/apquest)
- [Archipelago Docs](https://github.com/ArchipelagoMW/Archipelago/tree/main/docs)
- [Bizhawk Client](https://github.com/ArchipelagoMW/Archipelago/tree/main/worlds/_bizhawk)
- [Data Crystal RAM Map](https://datacrystal.tcrf.net/wiki/Mike_Tyson's_Punch-Out!!/RAM_map)
- [Data Crystal ROM Map](https://datacrystal.tcrf.net/wiki/Mike_Tyson's_Punch-Out!!/ROM_map)
- [MTPO Disassembly](https://github.com/nmikstas/mike-tysons-punch-out-disassembly/blob/master/source_files/Mike_Tysons_Punchout_Defines.asm)

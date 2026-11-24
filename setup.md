# Mike Tyson's Punch-Out!! Archipelago Setup Guide
## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [MTPO APworld](https://github.com/Landapanda/Mike-Tysons-Punch-Out-Archipelago/releases/latest)
- [Bizhawk](https://github.com/TASEmulators/BizHawk/releases/latest)
- MTPO ROM. Both editions of Tyson as well as the Mr. Dream version should work. If any version doesn't work please let me know!
## Configuring BizHawk
- For MTPO it is recommended to use the NESHawk core rather than QuickNES because the game seems to run better on the former. 
- In Config > Customize, enable "Run in Background" to prevent disconnects while the game runs in the background.
- Due to the nature of the game and how the AP currently works, it is recommended to set a hotkey for Soft Reset. (Config > Hotkeys > Soft Reset)

## Connecting to the Game/Client/Server
1. Open the Bizhawk Client through the Archipelago Launcher or the exe itself.
2. Open Bizhawk (Emuhawk) and load the your ROM in the emulator.
3. After the game is loaded, click on Tools > Lua Console. 
4. On the Lua Console window, click Script > Open Script or press Ctrl+O.
5. On the file dialog, navigate to your Archipelago folder in then data/lua/ and select "connector_bizhawk_generic.lua"
6. Bizhawk and the Lua Console may freeze for a couple of seconds, just wait until it starts to print "Looking for client..." in the output.
7. Shortly after it should connect to the Bizhawk Client and will print "Client Connected" in the output box and "Connected to Bizhawk" in the client.
8. Connect to your Archipelago server in the Bizhawk Client and you should be ready to play!
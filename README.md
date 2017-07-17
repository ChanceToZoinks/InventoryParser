# InventoryParser
Path of Exile inventory value calculator

This tool calculates the total value of all currency, maps and unique maps held in the selected character's inventory based on the poe.ninja prices. The chaos/hr is displayed so you can track efficiency of certain farming or other moneymaking methods. The tool also tracks the current zone you're in, but that's mostly just cosmetic at the moment. Eventually the zone tracking will be used to gather historical data as a way to compare the money making efficiency of any given zone.

When I started working on this I had been programming in Python for about 2 days, so there will probably be many many refactors needed, and already I can see issues with my choice of implementation. 

TODO: Multithread. Add more features :^)

Note: At the time of this readme update Python 3.6 isn't supported by py2exe or pyinstaller yet so to run this you have to download it and run GUIMain with python3.6 interpreter. Eventually I'll get around to installing an older python version and packaging it for distribution. I need to multithread it first though.

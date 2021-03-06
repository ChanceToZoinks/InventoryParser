"""Every time a zone is entered Path of Exile\logs\client.txt is updated with a block of text. This block of text
   indicates the current step in the connection process and identifies the zone being entered. Each update block takes
   the form:

   2017/07/13 04:17:11 48766015 857 [DEBUG Client 460] Got Instance Details from login server
   2017/07/13 04:17:11 48766015 873 [INFO Client 460] Just before calling client instance session
   2017/07/13 04:17:11 48766015 d5 [INFO Client 460] Connecting to instance server at 158.85.40.109:6112
   2017/07/13 04:17:11 48766062 119 [DEBUG Client 460] Connect time to instance server was 31ms
   2017/07/13 04:17:11 48766140 6f [INFO Client 460] Tile hash: 3011923282
   2017/07/13 04:17:11 48766140 70 [INFO Client 460] Doodad hash: 0
   2017/07/13 04:17:11 48766406 6e7 [DEBUG Client 460] Joined guild named [Guild Name Here] with X members
   2017/07/13 04:17:11 48766515 951 [INFO Client 460] : You have entered Highgate.
   2017/07/13 04:17:11 48766609 a1d [DEBUG Client 460] Entering area 2_4_town

   We are specifically interested in these two lines:

   2017/07/13 04:17:11 48766140 6f [INFO Client 460] Tile hash: 3011923282
   2017/07/13 04:17:11 48766609 a1d [DEBUG Client 460] Entering area 2_4_town

   The tile hash is a hashed unique identifier for every zone that doesn't appear to change at any point.
   The second line tells us the internal name of the zone and in the case of non-map zones identifies both difficulty
   and act. There is a third piece (and in some rare cases a fourth) to the second line that indicates the area of the
   act the player is in. In the case of the example above 2_4_town tells us that the player has entered Cruel Act 4
   Town. Dried Lake in Cruel is identified by 2_4_2. It appears that with the exception of the town the third piece of
   the identifier is a number starting with one and going to N (where N is the number of zones in the act). The number
   appears to be based on the order the player must progress through the zones. So, for example, Cruel Aqueduct is
   identified by 2_4_1 because it is the first zone in Act 4 in the Cruel difficulty.

   Maps are handled differently as can be seen here:

   2017/07/13 04:17:46 48801406 a1d [DEBUG Client 460] Entering area MapAtlasDesert

   This line appears to tell us the internal name for each zone; this name corresponds to a unique tile hash. With these
   two pieces of information it is possible to track which zone the player is currently in and which zones they have
   previously been in. This is important because it allows us to compare potential farming spots more accurately than
   simply resetting xp every now and then and "eyeballing it." It also allows us to compare zones based on the amount of
   wealth being generated in each zone over a period of time. Although, it should be noted that since the game is RNG
   based simply comparing chaos/time between zones isn't always going to be a good way to compare the economic
   efficiency of a given zone to another. With that said this should prove useful for targeted farming such as was done
   in Legacy league with the use of IIQ and Spider Forest Map.
"""
from itertools import islice
import os

# 'zone_history' keeps track of every zone a player enters
# this is important so historical data can be gathered on each zone.
zone_history = []

# 'current_zone'  is updated on zone change
current_zone = ''


def zone_changed(temp_name):
    """when a zone changes this is called"""

    global current_zone

    # overwrite the current zone hash and zone name
    current_zone = temp_name

    zone_history.append(temp_name.rstrip('\n'))

    print('zone changed.\ncurrent zone: ' + str(current_zone.rstrip('\n')))
    print('zones visited this session: ' + str(zone_history))

# the reversed_lines, reversed_block and check_last_5_lines functions were found here:
# https://stackoverflow.com/questions/260273/most-efficient-way-to-search-the-last-x-lines-of-a-file-in-python


def reversed_lines(file):
    """Generate the lines of file in reverse order."""

    part = ''
    for block in reversed_blocks(file):
        for c in reversed(block):
            if c == '\n' and part:
                yield part[::-1]
                part = ''
            part += c
    if part:
        yield part[::-1]


def reversed_blocks(file, blocksize=4096):
    """Generate blocks of file's contents in reverse order."""

    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)


def check_last_5_lines(file, key):
    """searching the last 5 lines of the file because the last 5 lines in Client.txt contain the info needed"""

    for line in islice(reversed_lines(file), 5):
        # first set tile hash then set zone name
        if key in line.rstrip('\n'):
            temp_zone_name = line.split(key, 1)[1]
            # if the most recent tile hash found isn't the current tile hash then we change the current tile hash
            if not temp_zone_name == current_zone:
                zone_changed(temp_zone_name)

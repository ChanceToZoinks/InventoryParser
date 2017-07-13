"""Every time a zone is entered Path of Exile\logs\client.txt is updated with a block of text. This block of text
   indicates the current step in the connection process and identifies the zone being entered each update block takes
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
   and act. There is a third piece to the second line that indicates the area of the act the player is in. In the case
   of the example above 2_4_town tells us that the player has entered Cruel Act 4 Town. Dried Lake in Cruel is
   identified by 2_4_2. It appears that with the exception of the town the third piece of the identifier is a number
   starting with one and going to N (where N is the number of zones in the act). The number appears to be based on the
   order the player must progress through the zones. So for example Cruel Aqueduct is identified by 2_4_1 because it is
   the first zone in Act 4 in the Cruel difficulty.

   Maps are handled differently as can be seen here:

   2017/07/13 04:17:46 48801406 a1d [DEBUG Client 460] Entering area MapAtlasDesert

   This line appears to tell us the internal name for each zone; this name corresponds to a unique tile hash. With these
   two pieces of information it is possible to track which zone the player is currently in and which zones they have
   previously been in. This is important because it allows us to compare potential farming spots more accurately than
   simply resetting xp every now and then and "eyeballing it." It also allows us to compare zones based on the amount of
   wealth being generated in each zone over a period of time; although, it should be noted that since the game is RNG
   based simply comparing chaos/time between zones isn't always going to be a good way to determine the economic
   efficiency of a given zone to another. With that said this should prove useful for targeted farming such as was done
   in Legacy league with the use of IIQ and Spider Forest Map.
"""

import PlayerTrackerHelper


# 'zone_history' keeps track of every zone a player enters and the corresponding Tile hash
# this is important so historical data can be gathered on each zone. zone_history is zipped from two lists in helper
zone_history = {}

tile_hash = []
zone_name = []

# 'current_zone' takes the form tile_hash:zone_name and is updated on zone change by the helper
current_zone = {'tile_hash': '', 'zone_name': ''}


def zone_changed(temp_hash, temp_name):
    """the helper calls this method to notify the tracker that a zone change has occurred"""

    global zone_history

    # overwrite the current zone hash and zone name
    current_zone['tile_hash'] = temp_hash
    current_zone['zone_name'] = temp_name
    zone_history = dict(zip(tile_hash, zone_name))
    print('zone changed')
    print('current zone: ' + str(current_zone))
    print('zones visited this session: ')
    print(zone_history)

PlayerTrackerHelper.start_tracking()

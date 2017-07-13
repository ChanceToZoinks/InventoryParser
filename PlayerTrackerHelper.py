import time
import sys

named_libs = [('UserData', 'User')]
for (name, short) in named_libs:
    try:
        lib = __import__(name)
    except ImportError:
        print(sys.exc_info())
    else:
        globals()[short] = lib


# the method for monitoring whether or not a file changes in real time was found here:
# https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def start_tracking():
    """this method opens the client.txt file and monitors it for changes then notifies the tracker of changes"""

    import PlayerTracker

    logfile = open(User.client_txt_path, "r")
    loglines = follow(logfile)
    for line in loglines:
        if 'Tile hash: ' in line:
            temp_hash = line.split('Tile hash: ', 1)[1].rstrip('\n')
            if temp_hash not in PlayerTracker.tile_hash:
                # this line adds the tile hash to the appropriate list and strips the newline character at the end
                PlayerTracker.tile_hash.append(temp_hash)
        elif 'Entering area ' in line:
            temp_name = line.split('Entering area ', 1)[1].rstrip('\n')
            if temp_name not in PlayerTracker.zone_name:
                PlayerTracker.zone_name.append(temp_name)
                PlayerTracker.zone_changed(temp_hash, temp_name)

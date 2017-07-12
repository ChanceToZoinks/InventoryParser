import sys

named_libs = [('requests', 'requests'), ('UserData', 'User'), ('MarketDataGrabber', 'Market')]
for (name, short) in named_libs:
    try:
        lib = __import__(name)
    except ImportError:
        print(sys.exc_info())
    else:
        globals()[short] = lib


api_endpoint = 'https://www.pathofexile.com/character-window/get-items'


# pass account name, character name and the cookie. the cookie is necessary to access inventory other than equipped
PARAMS = {'accountName': User.account_name, 'character': User.character_name}
COOKIE = {'POESESSID': User.poesessid}


r = requests.get(url=api_endpoint, params=PARAMS, cookies=COOKIE)

print(r.status_code)

inventory_dict = r.json()
items = inventory_dict['items']


money = {'Chaos Orb': 0, 'Orb of Alchemy': 0, "Cartographer's Chisel": 0, 'Orb of Alteration': 0, 'Orb of Scouring': 0,
         'Orb of Augmentation': 0, 'Vaal Orb': 0, 'Exalted Orb': 0, 'Divine Orb': 0, "Glassblower's Bauble": 0,
         "Blacksmith's Whetstone": 0, "Armourer's Scrap": 0, 'Orb of Chance': 0, 'Orb of Regret': 0, 'Regal Orb': 0,
         'Orb of Transmutation': 0, 'Chromatic Orb': 0, 'Orb of Fusing': 0, "Jeweller's Orb": 0, 'Silver Coin': 0,
         'Scroll of Wisdom': 0, 'Portal Scroll': 0, "Gemcutter's Prism": 0, 'Blessed Orb': 0}

maps = {}

unique_maps = {}

total_chaos = 0

for item in items:
    if item['typeLine'] in money:
        money[item['typeLine']] += item['stackSize']
    elif 'Map' in item['typeLine']:
        if not maps.__contains__(item['typeLine']):
            maps[item['typeLine']] = 0
        maps[item['typeLine']] += 1


# def import_map_data():
#     """imports all maps and unique maps from poe.ninja into the corresponding dicts for easy access"""
#
#     global maps
#     global unique_maps


def calculate_total_in_chaos():
    """totals up the chaos value of all currency/maps in inventory each call"""

    global total_chaos

    # grab ratios from MarketDataGrabber and calculate total value in chaos
    for k in money:
        if k == 'Chaos Orb':
            total_chaos += money[k]
        elif k == 'Orb of Alchemy':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == "Cartographer's Chisel":
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Alteration':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Scouring':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Augmentation':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Vaal Orb':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Exalted Orb':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Divine Orb':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == "Glassblower's Bauble":
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == "Blacksmith's Whetstone":
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == "Armourer's Scrap":
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Chance':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Regret':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Regal Orb':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Transmutation':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Chromatic Orb':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Orb of Fusing':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == "Jeweller's Orb":
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Silver Coin':
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == "Gemcutter's Prism":
            total_chaos += money[k] * Market.item_value_search(k)
        elif k == 'Blessed Orb':
            total_chaos += money[k] * Market.item_value_search(k)

    for m in maps:
        total_chaos += maps[m] * Market.item_value_search(m, 'map')

calculate_total_in_chaos()

print(total_chaos)

# TODO: GRAB MAP DATA FROM POE.NINJA THEN FILL THE DICTS THEN CHECK EACH MAP AGAINST UNIQUE MAP IF NOT UNIQUE FIGURE OUT
# TODO: BASE MAP TYPE AND UPDATE COUNTS THEN CONVERT COUNTS TO CHAOS VALUE AND BOOM DONE

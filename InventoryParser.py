import sys

named_libs = [('requests', 'requests'), ('UserData', 'User'), ('MarketDataGrabber', 'Market')]
for (name, short) in named_libs:
    try:
        lib = __import__(name)
    except ImportError:
        print(sys.exc_info())
    else:
        globals()[short] = lib


"""this contains all the methods/data members necessary to parse a character's inventory and determine value in chaos
   'import_item_data()' should always be run before 'count_items_in_inventory()' followed by 'calculate..chaos()'
"""

api_endpoint = 'https://www.pathofexile.com/character-window/get-items'


# pass account name, character name and the cookie. the cookie is necessary to access inventory other than equipped
PARAMS = {'accountName': User.account_name, 'character': User.character_name}
COOKIE = {'POESESSID': User.poesessid}


r = requests.get(url=api_endpoint, params=PARAMS, cookies=COOKIE)


inventory_dict = r.json()
items = inventory_dict['items']

# 'money' has a hardcoded key:value {'Chaos Orb': 0} because the poe.ninja api doesn't include chaos orbs
# this is due to the fact that all other currency values are based on chaos so it is unnecessary to tell people
# that 1 chaos orb sells for 1 chaos orb
money = {'Chaos Orb': 0}

# 'not_money' contains a list of words to exclude from searches since poe.ninja doesn't list their chaos ratio
not_money = ['Alteration Shard', 'Scroll Fragment', 'Alchemy Shard', 'Transmutation Shard']

maps = {}

unique_maps = {}


def import_item_data():
    """imports all relevant items into corresponding dicts"""

    # check to see if money already contains each currency found in the poe.ninja api if not create a key for it value=0
    for c in Market.currency_market_data['lines']:
        if not c['currencyTypeName'] in money:
            money[c['currencyTypeName']] = 0

    # check to see if maps already contains each map found in the poe.ninja api if not create a key for it value=0
    for m in Market.map_market_data['lines']:
        if not m['baseType'] in maps:
            maps[m['baseType']] = 0

    # check to see if u_maps already contains each u_map found in the poe.ninja api if not create a key for it value=0
    for u_m in Market.unique_map_market_data['lines']:
        if not u_m['name'] in unique_maps:
            unique_maps[u_m['name']] = 0


def count_items_in_inventory():
    """counts the currency in the player inventory and assigns the value of the corresponding dict entry to the total"""

    for item in items:
        # frameType == 5 is checking for currency, fairly certain this is faster than comparing strings
        # also check to see if 'not_money' contains the item in question, if so ignore it
        if item['frameType'] == 5 and not not_money.__contains__(item['typeLine']):
            money[item['typeLine']] += item['stackSize']
        # first determine if the item is a map and that it is not unique (frameType == 3)
        # second iterate over all non-unique maps and compare the base type with the 'typeLine' of the map in question
        # once the base type is determined add one to the count of that map in the dict 'maps'
        # this is necessary because blue maps have a 'typeLine' that includes both base type and modifiers
        # this method also works for rare and normal maps so it solves all problems with one solution
        elif 'Map' in item['typeLine'] and item['frameType'] != 3:
            for m in maps:
                if m in item['typeLine']:
                    maps[m] += 1
        # if the map is unique add one to the count of that unique map in the dict 'unique_maps'
        elif 'Map' in item['typeLine'] and item['frameType'] == 3:
            for u_m in unique_maps:
                if u_m in item['name']:
                    unique_maps[u_m] += 1


total_in_chaos = 0


def calculate_total_in_chaos():
    """each call totals up the chaos value of all currency/maps in the dicts: 'currency', 'maps', 'unique maps'"""

    global total_in_chaos

    for k in money:
        # this is necessary because all other values are in chaos ratio so chaos doesn't have a value in poe.ninja api
        if k == 'Chaos Orb':
            total_in_chaos += money[k]
        else:
            total_in_chaos += money[k] * Market.item_value_search(k)

    for m in maps:
        total_in_chaos += maps[m] * Market.item_value_search(m, 'm')

    for u_m in unique_maps:
        total_in_chaos += unique_maps[u_m] * Market.item_value_search(u_m, 'u_m')


import_item_data()
count_items_in_inventory()
calculate_total_in_chaos()

print(total_in_chaos)
print(money)
print(maps)

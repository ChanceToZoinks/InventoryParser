"""this contains all the methods/data members necessary to parse a character's inventory and determine value in chaos
   'import_item_data()' should always be run before 'count_items_in_inventory()' followed by 'calculate..chaos()'
"""

import MarketDataGrabber as Market
import UserData as User
import requests
import time

# this is to calculate the chaos/hour
start_time = time.time()

# this holds the json data from the pathofexile.com api
items = {}

# this holds the money types from poe.ninja
money = {}

# 'not_money' contains a list of words to exclude from searches since poe.ninja doesn't list their chaos ratio
not_money = ['Alteration Shard', 'Scroll Fragment', 'Alchemy Shard', 'Transmutation Shard']

maps = {}

unique_maps = {}

total_in_chaos = 0

chaos_stamps = []

chaos_per_second = 0

chaos_per_hour = 0


def get_items_in_inventory():
    """call this to get all items in the player's inventory"""

    global items

    api_endpoint = 'https://www.pathofexile.com/character-window/get-items'

    # pass account name, character name and the cookie. the cookie is necessary to access inventory other than equipped
    params = {'accountName': User.account_name, 'character': User.character_name}
    cookie = {'POESESSID': User.poesessid}
    # TODO: make sure the poesessid hasn't expired and if it has update it

    r = requests.get(url=api_endpoint, params=params, cookies=cookie)

    inventory_dict = r.json()
    items = inventory_dict['items']


def import_item_data():
    """imports all relevant items into corresponding dicts"""

    # check to see if money already contains each currency found in the poe.ninja api if not create a key for it value=0
    for c in Market.currency_market_data['currencyDetails']:
        if not c['name'] in money:
            money[c['name']] = 0

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

    get_items_in_inventory()
    # first set all values in money, maps and unique_maps to 0 so they can be counted again
    # this ensures duplication doesnt arise since we dont store the unique ID of each currency from the poe api
    for c in money:
        money[c] = 0
    for m in maps:
        maps[m] = 0
    for um in unique_maps:
        unique_maps[um] = 0
    # then count the items
    for item in items:
        # frameType == 5 is checking for currency, fairly certain this is faster than comparing strings
        # also check to see if 'not_money' contains the item in question, if so ignore it
        if item['frameType'] == 5 and item['typeLine'] not in not_money:
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


def calculate_total_in_chaos():
    """each call totals up the chaos value of all currency/maps in the dicts: 'currency', 'maps', 'unique maps'"""

    global total_in_chaos
    global chaos_per_hour
    global chaos_per_second
    global chaos_stamps

    # keep track of the last 10 chaos values so an average/time can be established
    if len(chaos_stamps) > 10:
        chaos_stamps = chaos_stamps[1:]
        chaos_stamps.append(total_in_chaos)
    else:
        chaos_stamps.append(total_in_chaos)

    # we have to reset total in chaos each time so it doesn't just increase constantly
    total_in_chaos = 0
    for k in money:
        # this is necessary because all other values are in chaos ratio so chaos doesn't have a value in poe.ninja api
        if k == 'Chaos Orb':
            total_in_chaos += money[k]
        elif Market.item_value_search(k) is None:
            # values that return None from poe.ninja means no market data was found so they can't be calculated in chaos
            total_in_chaos += money[k] * 0
        else:
            total_in_chaos += money[k] * Market.item_value_search(k)

    for m in maps:
        total_in_chaos += maps[m] * Market.item_value_search(m, 'm')

    for u_m in unique_maps:
        total_in_chaos += unique_maps[u_m] * Market.item_value_search(u_m, 'u_m')

    total = 0
    for x in chaos_stamps:
        total += x
    average_chaos = total / len(chaos_stamps)
    chaos_per_second = average_chaos / (time.time() - start_time)
    chaos_per_hour = 3600 * chaos_per_second


item_data_imported_flag = 0


def inventory_data_setup():
    """populates necessary data. exists so we can be sure UserData has been setup first"""

    global item_data_imported_flag

    # check if the data has already been imported
    if item_data_imported_flag == 0:
        Market.load_market_data()
        import_item_data()
        item_data_imported_flag += 1


def count_and_calc():
    """this solely exists so GUIMain can call one method to calculate the value of the inventory"""

    count_items_in_inventory()
    calculate_total_in_chaos()

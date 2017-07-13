import sys

named_libs = [('requests', 'requests'), ('UserData', 'User'), ('MarketDataGrabber', 'Market')]
for (name, short) in named_libs:
    try:
        lib = __import__(name)
    except ImportError:
        print(sys.exc_info())
    else:
        globals()[short] = lib


"""this contains all the methods/data members necessary to parse a character's inventory and determine value in chaos"""

api_endpoint = 'https://www.pathofexile.com/character-window/get-items'


# pass account name, character name and the cookie. the cookie is necessary to access inventory other than equipped
PARAMS = {'accountName': User.account_name, 'character': User.character_name}
COOKIE = {'POESESSID': User.poesessid}


r = requests.get(url=api_endpoint, params=PARAMS, cookies=COOKIE)


inventory_dict = r.json()
items = inventory_dict['items']


money = {}

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


def count_currency_in_inventory():
    """counts the currency in the player inventory and assigns the value of the corresponding dict entry to the total"""




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
calculate_total_in_chaos()

print(total_in_chaos)

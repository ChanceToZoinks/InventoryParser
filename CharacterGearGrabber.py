import UserData as User
import requests

gear_resists = {'helm': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'bodyarmour': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'gloves': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'boots': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'belt': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'amulet': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'ring': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'ring2': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'weapon': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'offhand': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True},
                'passivejewels': {'fire': 0, 'cold': 0, 'lightning': 0}
                }

totals = {'fire': 0, 'cold': 0, 'lightning': 0}

gear_api_endpoint = 'https://www.pathofexile.com/character-window/get-items'
jewel_api_endpoint = 'https://www.pathofexile.com/character-window/get-passive-skills'


def grab_inventory_data(use_jewels=False):
    """grabs inventory from ggg api and loads the local data with it"""

    User.load_user_data()

    params = {'accountName': User.account_name, 'character': User.character_name}
    cookie = {'POESESSID': User.poesessid}

    r = requests.get(gear_api_endpoint, params=params, cookies=cookie)
    g = r.json()
    items = g['items']

    for item in items:
        if item['inventoryId'].lower() in gear_resists:
            if item.get('craftedMods') is not None:
                for resist in item['craftedMods']:
                    if 'resistance' in resist.lower():
                        parse_gear(item, resist.lower())
            if item.get('implicitMods') is not None:
                for resist in item['implicitMods']:
                    if 'resistance' in resist.lower():
                        parse_gear(item, resist.lower())
            for resist in item['explicitMods']:
                # explicit mods in the json formatted "+#% to X Resistance" so strip '+' and split at % to get number
                if 'resistance' in resist.lower():
                    parse_gear(item, resist.lower())
            # if the item has 6 mods, has been crafted or is unique it can't be crafted again (unless u scour the craft)
            if len(item['explicitMods']) == 6 or item.get('craftedMods') is not None or item['frameType'] == 3:
                gear_resists[item['inventoryId'].lower()]['craftable'] = False
            else:
                gear_resists[item['inventoryId'].lower()]['craftable'] = True

    if use_jewels:
        r = requests.get(jewel_api_endpoint, params=params, cookies=cookie)
        j = r.json()
        items = j['items']

        for item in items:
            if item['inventoryId'].lower() in gear_resists:
                for resist in item['explicitMods']:
                    if 'resistance' in resist.lower():
                        parse_gear(item, resist.lower())


def parse_gear(item, resist_string):
    if 'fire' in resist_string.lower():
        gear_resists[item['inventoryId'].lower()]['fire'] += int(resist_string.strip('+').split('%', 1)[0])
    if 'cold' in resist_string.lower():
        gear_resists[item['inventoryId'].lower()]['cold'] += int(resist_string.strip('+').split('%', 1)[0])
    if 'lightning' in resist_string.lower():
        gear_resists[item['inventoryId'].lower()]['lightning'] += int(
            resist_string.strip('+').split('%', 1)[0])


def calculate_totals():
    for piece in gear_resists:
        totals['fire'] += gear_resists[piece]['fire']
        totals['cold'] += gear_resists[piece]['cold']
        totals['lightning'] += gear_resists[piece]['lightning']

grab_inventory_data(use_jewels=True)
calculate_totals()
print(gear_resists)
print(totals)

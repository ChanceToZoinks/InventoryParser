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
                'offhand': {'fire': 0, 'cold': 0, 'lightning': 0, 'craftable': True}
                }

gear_api_endpoint = 'https://www.pathofexile.com/character-window/get-items'


def grab_inventory_data():
    """grabs inventory from ggg api and loads the local data with it"""

    User.load_user_data()

    params = {'accountName': User.account_name, 'character': User.character_name}
    cookie = {'POESESSID': User.poesessid}

    r = requests.get(gear_api_endpoint, params=params, cookies=cookie)
    i = r.json()
    items = i['items']

    for item in items:
        if item['inventoryId'].lower() in gear_resists:
            for resist in item['explicitMods']:
                # explicit mods in the json formatted "+#% to X Resistance" so strip '+' and split at % to get number
                if 'resistance' in resist.lower():
                    if 'fire' in resist.lower():
                        gear_resists[item['inventoryId'].lower()]['fire'] += int(resist.strip('+').split('%', 1)[0])
                    elif 'cold' in resist.lower():
                        gear_resists[item['inventoryId'].lower()]['cold'] += int(resist.strip('+').split('%', 1)[0])
                    elif 'lightning' in resist.lower():
                        gear_resists[item['inventoryId'].lower()]['lightning'] += int(resist.strip('+').split('%', 1)[0])
            # if the item has 6 mods, has been crafted or is unique it can't be crafted again (unless u scour the craft)
            if len(item['explicitMods']) == 6 or item.get('craftedMods') is not None or item['frameType'] == 3:
                gear_resists[item['inventoryId'].lower()]['craftable'] = False
            else:
                gear_resists[item['inventoryId'].lower()]['craftable'] = True

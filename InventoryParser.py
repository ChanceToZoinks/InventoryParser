import requests
import UserData as User

api_endpoint = 'https://www.pathofexile.com/character-window/get-items'


# pass account name, character name and the cookie. the cookie is necessary to access inventory other than equipped
PARAMS = {'accountName': User.account_name, 'character': User.character_name}
COOKIE = {'POESESSID': User.poesessid}

r = requests.get(url=api_endpoint, params=PARAMS, cookies=COOKIE)


inventory_dict = r.json()

items = inventory_dict['items']

money = {'Chaos Orb': 0, 'Orb of Alchemy': 0, "Cartographer's Chisel": 0, 'Orb of Alteration': 0, 'Orb of Scouring': 0,
         'Orb of Augmentation': 0, 'Vaal Orb': 0, 'Exalted Orb': 0, 'Divine Orb': 0, "Glassblower's Bauble": 0,
         "Blacksmith's Whetstone": 0, "Armourer's Scrap": 0, 'Orb of Chance': 0, 'Orb of Regret': 0, 'Regal Orb': 0,
         'Orb of Transmutation': 0, 'Chromatic Orb': 0, 'Orb of Fusing': 0, "Jeweller's Orb": 0, 'Silver Coin': 0,
         'Scroll of Wisdom': 0, 'Portal Scroll': 0, "Gemcutter's Prism": 0, 'Blessed Orb': 0}

for item in items:
    if item['typeLine'] in money:
        money[item['typeLine']] += item['stackSize']


def total_in_chaos():
    total = 0
    for k in money:

        # hand coded ratios GIGANTIC pain in the ass. looking to update this later to automatically determine ratios
        # based on market data
        
        if k == 'Chaos Orb':
            total += money[k]
        elif k == 'Orb of Alchemy':
            total += money[k] / 3
        elif k == "Cartographer's Chisel":
            total += money[k] / 5
        elif k == 'Orb of Alteration':
            total += money[k] / 12
        elif k == 'Orb of Scouring':
            total += money[k] / 2
        elif k == 'Orb of Augmentation':
            total += money[k] / 30
        elif k == 'Vaal Orb':
            total += money[k]
        elif k == 'Exalted Orb':
            total += money[k] * 90
        elif k == 'Divine Orb':
            total += money[k] * 15
        elif k == "Glassblower's Bauble":
            total += money[k] / 4
        elif k == "Blacksmith's Whetstone":
            total += money[k] / 20
        elif k == "Armourer's Scrap":
            total += money[k] / 40
        elif k == 'Orb of Chance':
            total += money[k] / 8
        elif k == 'Orb of Regret':
            total += money[k]
        elif k == 'Regal Orb':
            total += money[k]
        elif k == 'Orb of Transmutation':
            total += money[k] / 40
        elif k == 'Chromatic Orb':
            total += money[k] / 12
        elif k == 'Orb of Fusing':
            total += money[k] / 3
        elif k == "Jeweller's Orb":
            total += money[k] / 10
        elif k == 'Silver Coin':
            total += money[k] / 5
        elif k == "Gemcutter's Prism":
            total += money[k]
        elif k == 'Blessed Orb':
            total += money[k] / 2

    return total

print(total_in_chaos())




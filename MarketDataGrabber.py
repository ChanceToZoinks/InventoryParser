import requests
import UserData as User

"""Grab the market data for currency and maps from poe.ninja"""

# poe.ninja doesn't require any kind of cookie or api key to access their data.
currency_api_endpoint = 'http://api.poe.ninja/api/Data/GetCurrencyOverview'
map_api_endpoint = 'http://api.poe.ninja/api/Data/GetMapOverview'
unique_map_api_endpoint = 'http://cdn.poe.ninja/api/Data/GetUniqueMapOverview'

# pass the league grabbed from UserData in GET request
PARAMS = {'league', User.league}

currency = requests.get(currency_api_endpoint, params=PARAMS)
maps = requests.get(map_api_endpoint, params=PARAMS)
unique_maps = requests.get(unique_map_api_endpoint, params=PARAMS)

# all data in dict form
currency_market_data = currency.json()
map_market_data = maps.json()
unique_map_market_data = unique_maps.json()


def item_value_search(item_to_search, item_type='currency'):
    """item and second argument indicating type 'currency' is default, 'map'/'unique map' options, returns value in c"""

    if item_type == 'currency':
        for item in currency_market_data['lines']:
            if item['currencyTypeName'] == str(item_to_search):
                return item['chaosEquivalent']
    elif item_type == 'map':
        for item in map_market_data['lines']:
            if item['name'] == str(item_to_search):
                return item['chaosValue']
    # elif item_type == 'unique map':
    #     for item in map_market_data['lines']:
    #         if item['name'] == str(item_to_search):
    #             return item['chaosValue']

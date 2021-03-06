"""Grab the market data for currency and maps from poe.ninja"""

import UserData as User
import requests


currency_api_endpoint = 'http://api.poe.ninja/api/Data/GetCurrencyOverview'
map_api_endpoint = 'http://api.poe.ninja/api/Data/GetMapOverview'
unique_map_api_endpoint = 'http://cdn.poe.ninja/api/Data/GetUniqueMapOverview'

# pass the league grabbed from UserData in GET request
PARAMS = {}

currency = None
maps = None
unique_maps = None

# all data in dict form
currency_market_data = {}
map_market_data = {}
unique_map_market_data = {}


def load_market_data():
    """this method loads the market data and exists so we can be sure the UserData is loaded
       this must ALWAYS be done before attempting to calculate value with the inventory parser
    """

    global PARAMS
    global currency
    global maps
    global unique_maps
    global currency_market_data
    global map_market_data
    global unique_map_market_data

    PARAMS = {'league': User.league}

    currency = requests.get(currency_api_endpoint, params=PARAMS)
    maps = requests.get(map_api_endpoint, params=PARAMS)
    unique_maps = requests.get(unique_map_api_endpoint, params=PARAMS)

    # all data in dict form
    currency_market_data = currency.json()
    map_market_data = maps.json()
    unique_map_market_data = unique_maps.json()


def item_value_search(item_to_search, item_type='c'):
    """item_type:'c' is default, 'm'/'u_m' optional ('m' means 'map', 'u_m' means 'unique map'), returns chaos value"""

    if item_type == 'c':
        for item in currency_market_data['lines']:
            if item['currencyTypeName'] == str(item_to_search):
                return item['chaosEquivalent']
    elif item_type == 'm':
        for item in map_market_data['lines']:
            if item['name'] == str(item_to_search):
                return item['chaosValue']
    elif item_type == 'u_m':
        for item in unique_map_market_data['lines']:
            if item['name'] == str(item_to_search):
                return item['chaosValue']

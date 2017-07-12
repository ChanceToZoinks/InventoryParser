import requests

# poe.ninja doesn't require any kind of cookie or api key to access their data.
url = 'http://api.poe.ninja/api/Data/GetCurrencyOverview?league=Legacy&date=2017-07-12'

r = requests.get(url)

print(r.status_code)

data = r.json()

print(data)
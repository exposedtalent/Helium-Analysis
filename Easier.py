import requests
import pprint
import json
from datetime import datetime
# Using this we can change the hotspot by just putting in the value of the Hotspoot network address
hotspot = ('h1124jdKvWJeBxShhSuwC135xG7jmV55iLchtQxtELj65DHwP56ZY')
url = ('https://api.helium.io/v1/hotspots/' + hotspot + '/activity')
# We get the json file from the url
response = requests.get(url)
data = response.json()
# add a cursor variable to go to next pages of the data
# cursor = data['cursor']

# data = response.json()
# f = open(response)
# data = json.load(f)

print(data)
# for i in data['data']:
#     if(i['type'] == "popoc_receipts_v1"):
#         time = datetime.fromtimestamp(i['time']).strftime('%Y-%m-%d-%H:%M:%S')
#         print(time, i['path'])
    
    
# for i in data['data']:
#    print(i)



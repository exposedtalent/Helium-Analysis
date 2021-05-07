import requests
from datetime import datetime
# Using this can change the network address
hotspot='112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg'
# Url for the helium api
url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
# using the request library to get the data into a json
response = requests.get(url)
output = response.json()
# cursor needded to go to next pages 
cursor = output['cursor']

# for loop to go throught the first page and print the data 
for i in output['data']:
    if (i['type'] == "poc_receipts_v1"):
        timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
        print(timestamp, i['path'][0]['challengee'], i['path'][0]['geocode']['short_street'], i['path'][0]['geocode']['short_city'], len(i['path'][0]['witnesses']))
        
# for loop to go thrught and print the data after using cursor to go to next page
url=url+'?cursor='+cursor
response = requests.get(url)
output = response.json()
for i in output['data']:
    if (i['type'] == "poc_receipts_v1"):
      timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
      print(timestamp, i['path'][0]['challengee'], i['path'][0]['geocode']['short_street'], i['path'][0]['geocode']['short_city'], len(i['path'][0]['witnesses']))

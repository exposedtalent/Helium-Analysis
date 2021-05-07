import requests
from datetime import datetime

hotspot='112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg'

url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
response = requests.get(url)
output = response.json()
cursor=output['cursor']
for i in output['data']:
    if (i['type'] == "poc_receipts_v1"):
      timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
      print(timestamp, i['path'][0]['challengee'], i['path'][0]['geocode']['short_street'], i['path'][0]['geocode']['short_city'], len(i['path'][0]['witnesses']))

url=url+'?cursor='+cursor
response = requests.get(url)
output = response.json()
for i in output['data']:
    if (i['type'] == "poc_receipts_v1"):
      timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
      print(timestamp, i['path'][0]['challengee'], i['path'][0]['geocode']['short_street'], i['path'][0]['geocode']['short_city'], len(i['path'][0]['witnesses']))

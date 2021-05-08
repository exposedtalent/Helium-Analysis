# TODO
# Remove the entire record if the own hotspot was an invalid witness
# Remove the witness if it's marked invalid
# Add an option to define how many pages to traverse/download
# Move the page traversal/download into a function that runs through a loop and appends all the data into one json object
# Prepare a summary and a detailed view
# Load the list of hotspots from a file

import requests
from datetime import datetime

def analyze_hotspot(hotspot, pagecount):
  output={"data": []}
  base_url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
  url = base_url
  while pagecount:
    response = requests.get(url)
    new_data = response.json()
    output['data'].extend(new_data['data']) 
    cursor=new_data['cursor']
    url=base_url+'?cursor='+cursor
    pagecount -= 1

  for i in output['data']:
    if (i['type'] == "poc_receipts_v1") and (i['path'][0]['challengee'] != hotspot):
      timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d-%I:%M:%S")
      challengee = i['path'][0]['challengee']
      print(timestamp, challengee, i['path'][0]['geocode']['short_street'], i['path'][0]['geocode']['short_city'], len(i['path'][0]['witnesses']))

hs_mg='112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg'
hs_ag='112Cggcbje3yS4a1YpfyVNt1B2DTYNqiFjwaNEvfJp6fhc8UPuLc'
hs_jh='112SDjb928fBrnhzLLLif1ZNowE9E8VYfkHLoQTUoUQtuijpaPVd'
hs_jc='112na4aZ1XZsFFtAwUxtEfvn1kkP37yQ8zaTVvYBBEfkMEUkyzhx'

#print("==================== "+ hs_mg + "===============")
#analyze_hotspot(hs_mg, 1)
print("==================== "+ hs_ag + "===============")
analyze_hotspot(hs_ag, 1)
#print "==================== "+ hs_jh + "==============="
#analyze_hotspot(hs_jh)
#print "==================== "+ hs_jc + "==============="
#analyze_hotspot(hs_jc)

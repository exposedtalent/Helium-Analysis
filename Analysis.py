import requests
import json
from datetime import datetime
from beeprint import pp
import pandas as pd

def get_data(hotspot):
    # Url for the helium api
    url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
    # using the request library to get the data into a json
    response = requests.get(url)
    output = response.json()
    # cursor needded to go to next pages 
    cursor = output['cursor']
    # create a dic to store the values 
    my_dict = {}
    my_dict['data'] = []
    # for loop to go throught the first page and print the data 
    for i in output['data']:
        if (i['type'] == "poc_receipts_v1"):
            timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
            challengee = i['path'][0]['challengee']
            street = i['path'][0]['geocode']['short_street']
            city = i['path'][0]['geocode']['short_city']
            witnesses = len(i['path'][0]['witnesses'])
            # insert the values into a dict 
            my_dict['data'].append({
                'TimeStamp' : timestamp,
                'Challengee' : challengee,
                'Street'    : street,
                'City'      : city,
                'Witnesses' : witnesses
                
            })
            
    # for loop to go throught and print the data after using cursor to go to next page
    url=url+'?cursor='+cursor
    response = requests.get(url)
    output = response.json()
    for i in output['data']:
        if (i['type'] == "poc_receipts_v1"):
            timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
            challengee = i['path'][0]['challengee']
            street = i['path'][0]['geocode']['short_street']
            city = i['path'][0]['geocode']['short_city']
            witnesses = len(i['path'][0]['witnesses'])
            # insert the values into a dict
            my_dict['data'].append({
                'TimeStamp' : timestamp,
                'Challengee' : challengee,
                'Street'    : street,
                'City'      : city,
                'Witnesses' : witnesses
                
            })
    # write the data into a json
    # with open('data.json', 'w') as outfile:
    #     json.dump(my_dict, outfile)
    return my_dict

data = get_data('112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg')
df = pd.DataFrame(data)
df.to_csv('hotspotData.csv')
df.to_excel('HotspotData.xlsx')
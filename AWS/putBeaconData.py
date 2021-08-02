import json
import boto3
import requests
from datetime import datetime
import pandas as pd
import numpy as np


dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):

    pageNum = 2
    table = dynamodb.Table('Users')
    response = table.scan()
    hotspot = response['Items']
    for i in range(len(hotspot)):
        data = analyze_beacons(hotspot[i]['HotspotAddr'], pageNum)
        if(data != []):
            putData(data, hotspot[i]['HotspotAddr'])
    return {
        'statusCode': 200,
        'body': data
    }
def putData(data, name):
    table = dynamodb.Table('HotspotBeacons')
    for i in range(len(data)):
        table.put_item(
            Item = {
                "Hotspot": name,
                "BeaconTime": data[i]['TimeStamp'],
                "Challengee": data[i]['Challengee'],
                "Witnesses": data[i]['Witnesses'],
            }    
        )
def analyze_beacons(hotspot, pagecount):
    tableList = []
    output={"data": []}    
    base_url='https://api.helium.io/v1/hotspots/' + hotspot + '/challenges'
    url = base_url
    isCursor = True
    count = 0
    # While loop to go thrrough the num of pages specified by the user and get all the data from the Helium api
    try:
        while pagecount > 0:
            response = requests.get(url)
            new_data = response.json()
            output['data'].extend(new_data['data'])
            cursor=new_data['cursor']
            url=base_url+'?cursor='+cursor
            pagecount -= 1
            count += 1
    except KeyError:
        print("Key")
    # For loop to parse the data coming from the json file
    for i in output['data']:
        if (i['type'] == "poc_receipts_v1") and (i['path'][0]['challengee'] == hotspot):
            epochtime = i['time']
            timestamp = datetime.fromtimestamp(epochtime).strftime("%Y-%m-%d:%I:%M:%Ss")
            challengee = i['path'][0]['challengee']
            witnesses = len(i['path'][0]['witnesses'])

            alltheData = {
                'TimeStamp' : timestamp,
                'Challengee' : challengee,
                'Witnesses' : witnesses
            }
            # Append all of it to the tableList
            tableList.append(alltheData)
    print(tableList)
    return tableList
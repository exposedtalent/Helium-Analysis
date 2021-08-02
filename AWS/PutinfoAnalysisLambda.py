import requests
import pandas as pd
import numpy as np
import json
from botocore.exceptions import ClientError
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table1 = dynamodb.Table('HotspotRewards')
table2 = dynamodb.Table('HeliumRewardsDict')   

def lambda_handler(event, context):

    table3 = dynamodb.Table("HeliumData")
    response = table3.scan()
    heliumData = response['Items']
    # Calling the get_rewards and putting the data into reward list
    get_rewards(heliumData)

    return {
        'statusCode': 200,
        'body': "success"
    }
def putData(rewardsList):
    for i in range(len(rewardsList)):
        table1.put_item(
            Item = {
                "Hotspot_Owner": rewardsList[i]['Hotspot_Owner'],
                "Hotspot_Address": rewardsList[i]['Hotspot_Address'],
                "Hotspot_Name": rewardsList[i]['Hotspot_Name'],
                "Synced_Status": rewardsList[i]['Synced_Status'],
                "Hotspot_24H_HNT": str(rewardsList[i]['Hotspot_24H_HNT']),
                "Change_24H": str(rewardsList[i]['Change_24H']),
                "Hotspot_30D_HNT":str(rewardsList[i]['Hotspot_30D_HNT']),
                "Wallet_Balance":str(rewardsList[i]['Wallet_Balance'])
            }    
        )
def putDataBalance(balanceDict):
    table2.put_item(
        Item = {
            'Name':'wifimist',
            'HNT_Price': str(balanceDict['HNT_Price']),
            'Hotspots_24H_HNT' : str(balanceDict['Hotspots_24H_HNT']),
            'Hotspots_24H_USD' : str(balanceDict['Hotspots_24H_USD']),
            'Hotspots_30D_HNT' : str(balanceDict['Hotspots_30D_HNT']),
            'Hotspots_30D_USD' : str(balanceDict['Hotspots_30D_USD']),
            'Total_HNT' : str(balanceDict['Total_HNT']),
            'Total_USD' : str(balanceDict['Total_USD']),
        }    
    )
# Function to get the reward summary of the given hotspots
def get_rewards(heliumData):
    # This is to figure out the time
    twentyfourHour = '-2%20day'
    thirtyDays = '-30%20day'
    # initlize the various lists
    rewardList = []
    total24hrs = []
    total30days = []
    rewardChange = []
    syncStatus = []
    balanceList = []
    
    # Binance API to get the current rate
    url='https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])
    
    
    # for loop to calculate the rewards and the acc
    
    for i  in range(len(heliumData)):
        # Check if the hotspot is syncing  
        url='https://api.helium.io/v1/hotspots/' + heliumData[i]['HotspotAddr'] 
        response = requests.get(url)
        new_data = response.json()
        height = new_data['data']['status']['height']
        block = new_data['data']['block']
        if(height == None or (block - height) >= 500):
            syncStatus.append("Not Synced")
        else:
            syncStatus.append("Synced")
        if(height != None  ):
            # URL for the 24 hours
            url='https://api.helium.io/v1/hotspots/' + heliumData[i]['HotspotAddr'] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
            response = requests.get(url)
            new_data = response.json()
            reward24hrs = new_data['data'][0]['total']
            reward2day = new_data['data'][1]['total']

            if(reward24hrs == 0 and reward2day == 0):
                change = 0
            else:
                change = (round((reward24hrs - reward2day) / reward2day * 100, 2))
            rewardChange.append(change)
            total24hrs.append(reward24hrs)
            
            # URL for the 30 days 
            url='https://api.helium.io/v1/hotspots/' + heliumData[i]['HotspotAddr'] + '/rewards/sum?min_time=' + thirtyDays
            response = requests.get(url)
            new_data = response.json()
            reward30days = new_data['data']['total']
            total30days.append(reward30days)
            
            # To get the account balance of the users
            url='https://api.helium.io/v1/accounts/' + heliumData[i]['AccountAddr'] + '/stats'
            response = requests.get(url)
            new_data = response.json()
            balance = new_data['data']['last_day'][0]['balance']
            balanceList.append(balance)
            
            # Put eveything into a dict
            rewardDict = {
                'Hotspot_Owner' : heliumData[i]['HostName'],
                'Hotspot_Address' : heliumData[i]['HotspotAddr'],
                'Hotspot_Name' : heliumData[i]['HotspotName'],
                'Synced_Status': syncStatus[i],
                'Hotspot_24H_HNT' : round(total24hrs[i], 2),
                'Change_24H' : rewardChange[i],
                'Hotspot_30D_HNT' : round(total30days[i], 2),
                'Wallet_Balance' : round(balanceList[i] / 100000000 , 2),

            }
            rewardList.append(rewardDict)
    putData(rewardList)
    # Calculations
    bal = sum(balanceList) / 100000000
    usdBal = bal * price
    
    balanceDict = {
        'HNT_Price': round(price, 2),
        'Hotspots_24H_HNT' : round(sum(total24hrs), 2),
        'Hotspots_24H_USD' : round(sum(total24hrs) * price, 2),
        'Hotspots_30D_HNT' : round(sum(total30days), 2),
        'Hotspots_30D_USD' : round(sum(total30days) * price, 2),
        'Total_HNT' : round(bal, 2),
        'Total_USD' : round(usdBal, 2),
        
    }
    putDataBalance(balanceDict)


import requests
import pandas as pd
import numpy as np
import json
from json2html import *


rewardList = []

def lambda_handler(event, context):

    # This is to figure out the time
    twentyfourHour = '-2%20day'
    thirtyDays = '-30%20day'

    # This is for getting the Hotspot Addr fromt the csv file
    col_list = ["Hopstop Addr"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    addr = list(np.concatenate(data).flat)
    
    # Get the Host's Name from csv
    col_list = ["Host Name"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    hostName = list(np.concatenate(data).flat)
    
    # Get the Hotspot Name in a list
    col_list2 = ["Hotspot Name"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list2)
    data = df.values
    hotspotName = list(np.concatenate(data).flat)
    
    # This is for getting the Hotspot Addr fromt the csv file
    col_list = ["Account Addr"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    accAddr = list(np.concatenate(data).flat)
    
    rewardList = get_rewards(addr, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr)
    
    # put the result into a json
    jsonList = json.dumps(rewardList, indent = 4)
    # datajson = json2html.convert(json = jsonList)
    # change to this for aws Lambda instead of print
    return{
        'statusCode' : 200,
        'body': jsonList
    }
    
    

def get_rewards(hotspot, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr):
    total24hrs = []
    total30days = []
    rewardChange = []
    
    for i in range(len(hotspot)):
        # URL for the 24 hours
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
        response = requests.get(url)
        new_data = response.json()
        reward24hrs = new_data['data'][0]['total']
        reward2day = new_data['data'][1]['total']
        change = (round((reward2day - reward24hrs ) / reward2day * 100, 2))
        rewardChange.append(change)
        total24hrs.append(reward24hrs)
        
        # URL for the 30 days 
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + thirtyDays
        response = requests.get(url)
        new_data = response.json()
        reward30days = new_data['data']['total']
        total30days.append(reward30days)

    
    # Append the dict into a list
    # Function to get tthe total balance of all accounts
    balanceList = []
    
    # Binance API to get the current rate
    url='https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])
    
    # For loop to get the account balance of the user
    for i in range(len(accAddr)):
        url='https://api.helium.io/v1/accounts/' + accAddr[i] + '/stats'
        response = requests.get(url)
        new_data = response.json()
        balance = new_data['data']['last_day'][0]['balance']
        balanceList.append(balance)
        
    # Calculations
    bal = sum(balanceList) / 100000000
    usdBal = bal * price
    for i in range(len(hotspot)):
        # Put eveything into a dict
        rewardDict = {
            'Hotspot_Owner' : hostName[i],
            'Hotspot_Address' : hotspot[i],
            'Hotspot_Name' : hotspotName[i],
            'Hotspot_24H_HNT' : round(total24hrs[i], 2),
            'Hotspot_24H_USD' : round(total24hrs[i] * price, 2),
            'Change_24H' : rewardChange[i],
            'Hotspot_30D_HNT' : round(total30days[i], 2),
            'Hotspot_30D_USD' : round(total30days[i] * price, 2),
            'Wallet_Balance' : round(balanceList[i] / 100000000 , 2),
            'Wallet_Balance_USD' : round((balanceList[i] / 100000000) * price , 2),
            
        }
        rewardList.append(rewardDict)
    
    balanceDict = {
        'Hotspots_24H_HNT' : round(sum(total24hrs), 2),
        'Hotspots_24H_USD' : round(sum(total24hrs) * price, 2),
        'Hotspots_30D_HNT' : round(sum(total30days), 2),
        'Hotspots_30D_USD' : round(sum(total30days) * price, 2),
        'Total_HNT' : round(bal, 2),
        'Total_USD' : round(usdBal, 2),
        
    }
    dataDict = {
            'Balance' : balanceDict,
            'Hotspots' : rewardList,
            
        }
    dataList = [dataDict]
    return dataList
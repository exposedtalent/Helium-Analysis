# This file needs to read from the helium API and print out the 30 day and 24 hours rewards for the hotspot
# need host name, adreres  of the hotspot, name of th hotspot into a cvs 
# cognito for aws
import requests
import pandas as pd
import numpy as np
import json

rewardList = []
# Function to get the rewards for the hotspots 
def get_rewards(hotspot, twentyfourHour, thirtyDays, hostName, hotspotName):
    #data = {'data' : [{ }] }
    
    # for i in range(len(hotspotList)):
    url='https://api.helium.io/v1/hotspots/' + hotspot + '/rewards/sum?min_time=' + twentyfourHour
    response = requests.get(url)
    new_data = response.json()
    reward24hrs = new_data['data']['total']
    
    url='https://api.helium.io/v1/hotspots/' + hotspot + '/rewards/sum?min_time=' + thirtyDays
    response = requests.get(url)
    new_data = response.json()
    reward30days = new_data['data']['total']
    
    
    data = {
        'Hotspot Owner' : hostName,
        'Hotspot Address' : hotspot,
        'Hotspot Name' : hotspotName,
        'Hotspot 24hrs reward' : round(reward24hrs, 2),
        'Hotspot 30 day reward' : round(reward30days, 2)
    }
    rewardList.append(data)
    return rewardList

def get_balance(addrList):
    balanceList = []
    url='https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])
    for i in range(len(addrList)):
        url='https://api.helium.io/v1/accounts/' + addrList[i] + '/stats'
        response = requests.get(url)
        new_data = response.json()
        balance = new_data['data']['last_day'][0]['balance']
        balanceList.append(balance)
    bal = sum(balanceList) / 100000000
    usdBal = bal * price
    data = {
        'Total Balance' : round(bal,2),
        'Total Balance in USD' : round(usdBal, 2)
    }
    rewardList.append(data)        
# Main Function
def main():
    # This is to figure out the time
    twentyfourHour = '-24%20hour'
    thirtyDays = '-30%20day'

    # This is for getting the Hotspot Addr fromt the csv file
    col_list = ["Hopstop Addr"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    addr = list(np.concatenate(data).flat)
    
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
    
    balanceList = list(np.concatenate(data).flat)
    for i in range(len(addr)):
        rewardList = get_rewards(addr[i], twentyfourHour, thirtyDays, hostName[i], hotspotName[i])
    
    get_balance(balanceList)
    jsonList = json.dumps(rewardList, indent=4)
    print(jsonList)

if __name__ == "__main__":
    main()

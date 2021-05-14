# This file needs to read from the helium API and print out the 30 day and 24 hours rewards for the hotspot
# need host name, adreres  of the hotspot, name of th hotspot into a cvs 
# cognito for aws
import requests
import pandas as pd
import numpy as np
import json

rewardList = []
# Function to get the rewards for the hotspots 
def get_rewards(hotspot, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr):
    total24hrs = []
    total30days = []
    for i in range(len(hotspot)):
        # URL for the 24 hours
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + twentyfourHour
        response = requests.get(url)
        new_data = response.json()
        reward24hrs = new_data['data']['total']
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
    print(len(hotspot))
    for i in range(len(hotspot)):
        # Put eveything into a dict
        rewardDict = {
            'Hotspot Owner' : hostName[i],
            'Hotspot Address' : hotspot[i],
            'Hotspot Name' : hotspotName[i],
            'Hotspot 24 hrs reward' : round(total24hrs[i], 2),
            'Hotspot 24 hrs USD' : round(total24hrs[i] * price, 2),
            'Hotspot 30 day reward' : round(total30days[i], 2),
            'Hotspot 30 day USD' : round(total30days[i] * price,2),
            'Wallet Balance' : round(balanceList[i] / 100000000 , 2),
            'Wallet Balance in USD' : round((balanceList[i] / 100000000) * price , 2),
            
        }
        rewardList.append(rewardDict)
    
    balanceDict = {
        'Hotspot 24hrs Total' : round(sum(total24hrs),2),
        'Hotspot 24 hrs USD' : round(sum(total24hrs) * price,2),
        'Hotspot 30 day Total' : round(sum(total30days),2),
        'Hotspot 30 day USD' : round(sum(total30days) * price,2),
        'Total Balance' : round(bal,2),
        'Total Balance in USD' : round(usdBal, 2),
        
    }
    dataDict = {
            'Balance' : balanceDict,
            'Hotspot' : rewardList
        }
    return dataDict
            
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
    
    # for loop to get rewards 
    
    rewardList = get_rewards(addr, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr)
    
    # put the result into a json
    jsonList = json.dumps(rewardList, indent=4)
    # change to this for aws Lambda
    # return{
    #     'statusCode' : 200,
    #     'body': jsonList
    # }
    print(jsonList)

if __name__ == "__main__":
    main()

import requests
import pandas as pd
import numpy as np
import json
import codecs
import time


rewardList = None
start_time = time.time()

def main():
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
    with open('data.json','w') as jsonFile:
        json.dump(rewardList, jsonFile)
    print("Process finished --- %s seconds ---" % (time.time() - start_time))
    
    # datajson = json2html.convert(json = jsonList)
    # change to this for aws Lambda instead of print
    # return{
    #     'statusCode' : 200,
    #     'body': jsonList
    # }
    
    

def get_rewards(hotspot, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr):
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
    
    for i  in range(len(hotspot)):
        # Check if the hotspot is syncing  
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] 
        response = requests.get(url)
        new_data = response.json()
        height = new_data['data']['status']['height']
        block = new_data['data']['block']
        if(height == None):
            syncStatus.append("Not Synced")
        elif((block - height) >= 250 ):
            syncStatus.append("Not Synced")
        else:
            syncStatus.append("Synced")
        if(height != None  ):
            # URL for the 24 hours
            url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
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
            url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + thirtyDays
            response = requests.get(url)
            new_data = response.json()
            reward30days = new_data['data']['total']
            total30days.append(reward30days)
            
            # To get the account balance of the users
            url='https://api.helium.io/v1/accounts/' + accAddr[i] + '/stats'
            response = requests.get(url)
            new_data = response.json()
            balance = new_data['data']['last_day'][0]['balance']
            balanceList.append(balance)
            
            # Put eveything into a dict
            rewardDict = {
                'Hotspot_Owner' : hostName[i],
                'Hotspot_Address' : hotspot[i],
                'Hotspot_Name' : hotspotName[i],
                'Hotspot_24H_HNT' : round(total24hrs[i], 2),
                'Hotspot_24H_USD' : round(total24hrs[i] * price, 2),
                'Change_24H' : rewardChange[i],
                'Synced_Status': syncStatus[i],
                'Hotspot_30D_HNT' : round(total30days[i], 2),
                'Hotspot_30D_USD' : round(total30days[i] * price, 2),
                'Wallet_Balance' : round(balanceList[i] / 100000000 , 2),
                'Wallet_Balance_USD' : round((balanceList[i] / 100000000) * price , 2),
            
            }
            rewardList.append(rewardDict)
            
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
    dataDict = {
            'Balance' : balanceDict,
            'Hotspots' : rewardList,
            
        }
    
    return dataDict

if __name__ == '__main__':
    main()
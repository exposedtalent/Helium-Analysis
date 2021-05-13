# This file needs to read from the helium API and print out the 30 day and 24 hours rewards for the hotspot
# need host name, adreres  of the hotspot, name of th hotspot into a cvs 
# cognito for aws
import requests
import json
import datetime
import pandas as pd
import csv
import numpy as np

# Function to get the rewards for the hotspots 
def get_rewards(hotspotList, minDate):
    rewardList = []
    for i in range(len(hotspotList)):
        url='https://api.helium.io/v1/hotspots/' + hotspotList[i] + '/rewards/sum?min_time=' + minDate
        response = requests.get(url)
        new_data = response.json()
        rewards = new_data['data']['total']
        rewardList.append(rewards)
    return rewardList

def get_balance(addrList):
    balanceList = []
    for i in range(len(addrList)):
        url='https://api.helium.io/v1/accounts/' + addrList[i] + '/stats'
        response = requests.get(url)
        new_data = response.json()
        balance = new_data['data']['last_day'][0]['balance']
        balanceList.append(balance)
    print("Total Balance : ", round(sum(balanceList) / 100000000, 2))
    
# Function to print out the result
def result(rewardList, hotspot) : 
    # Get the Host name in a list
    col_list = ["Host Name"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    hostName = list(np.concatenate(data).flat)
    
    # Get the Hotspot Name in a list
    col_list2 = ["Hotspot Name"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list2)
    data = df.values
    hotspotName = list(np.concatenate(data).flat)
    
    # For loop to print
    for i in range(len(hotspot)):
        print(
            " Host Name : ", hostName[i], "\n",
            "Hotspot Addr : ", hotspot[i], "\n",
            "Hotspot Name : " , hotspotName[i], "\n",
            "Rewards "  ,round(rewardList[i], 2), "\n"
        )
    print(" Reward Total: ", round(sum(rewardList),2), "\n")
    
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
    
    # This is for getting the Hotspot Addr fromt the csv file
    col_list = ["Account Addr"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    balanceList = list(np.concatenate(data).flat)
   
    # For loop to call the get_rewards function
    print("=================== 24 Hours ===================")
    rewardList = get_rewards(addr, twentyfourHour )
    result(rewardList,addr)
    print("=================== 30 DAY ===================")
    rewardList = get_rewards(addr, thirtyDays )
    result(rewardList,addr)
    print("=================== Total Balance ===================")
    get_balance(balanceList)

if __name__ == "__main__":
    main()

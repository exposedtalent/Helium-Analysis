import requests
import json
from datetime import datetime
from beeprint import pp
import pandas as pd
import csv
import numpy as np

def get_data(hotspot):
    url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
    # using the request library to get the data into a json
    response = requests.get(url)
    output = response.json()
    # cursor needded to go to next pages 
    cursor = output['cursor']
    # create a tableList to store the values 
    tableList = []
    # for loop to go throught the first page and print the data 
    for i in output['data']:
        if (i['type'] == "poc_receipts_v1"):
            timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
            challengee = i['path'][0]['challengee']
            street = i['path'][0]['geocode']['short_street']
            city = i['path'][0]['geocode']['short_city']
            witnesses = len(i['path'][0]['witnesses'])
            # insert the values into a dict 
            allthedata = {
                'TimeStamp' : timestamp,
                'Challengee' : challengee,
                'Street'    : street,
                'City'      : city,
                'Witnesses' : witnesses
            }
            tableList.append(allthedata)
            
            
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
            alltheData = {
                'TimeStamp' : timestamp,
                'Challengee' : challengee,
                'Street'    : street,
                'City'      : city,
                'Witnesses' : witnesses
            }
            tableList.append(alltheData)
    
    return tableList

def sortCSV(file):
    # after the file is written we need to sort the csv file using pandas library 
    df = pd.read_csv(file)
    sorted_df = df.sort_values(by=["Witnesses"], ascending=True)
    sorted_df.to_csv('Sorted_hotspotData.csv', index=False)
    
def summary(file):
    # Looks at only the Witnesses col and prints the num of Witnesses 
    col_list = ["Witnesses"]
    df = pd.read_csv(file, usecols=col_list)
    data = df.values
    
    # using the numpy lib we find the number of times this router has seen 1,2,3,4,5 or more witnesses for a challenge
    occurOne = np.count_nonzero(data == 1)
    occurTwo = np.count_nonzero(data == 2)
    occurThree = np.count_nonzero(data == 3)
    occurFour = np.count_nonzero(data == 4)
    occurFive = np.count_nonzero(data == 5)
    occurMore = np.count_nonzero(data > 5)
    numLines = occurOne + occurTwo + occurThree + occurFour + occurFive + occurMore
    print(
        "1 Witnesses : ", occurOne,"times\n" 
        "2 Witnesses : ", occurTwo,"times\n"
        "3 Witnesses : ", occurThree,"times\n"
        "4 Witnesses : ", occurFour,"times\n"
        "5 Witnesses : ", occurFive,"times\n"
        "More than 5 Witnesses :", occurMore, "times"
        )
    
    new_col_list = ["Challengee"]
    df2 = pd.read_csv(file, usecols=new_col_list)
    Challengee = df2
    usersDf = pd.read_csv(file,  skipfooter= numLines-occurOne, usecols = new_col_list, engine='python')
    print(df2.values)

    
    
    
# Need to print the routers that we are the only one to see 
def details(file):
    new_col_list = ["Challengee"]
    # df = pd.read_csv(file, usecols=col_list)
    
    usersDf = pd.read_csv(file,  skipfooter= 60, usecols = new_col_list, engine='python')
    print(usersDf.values)
   
# Update as needed 
# Change the Network Adderess for different ones
data = get_data('112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg')
df = pd.DataFrame(data)
df.to_csv('hotspotData.csv')
sortCSV('hotspotData.csv')
summary('Sorted_hotspotData.csv')



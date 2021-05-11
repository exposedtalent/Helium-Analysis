# TODO
# Remove the entire record if the own hotspot was an invalid witness
# Remove the witness if it's marked invalid
# Load the list of hotspots from a file

# Imports
import requests
import json
from datetime import datetime
import pprint
import pandas as pd
import csv
import numpy as np

def get_reward_scale(challengee):
    base_url='https://api.helium.io/v1/hotspots/' + challengee
    response = requests.get(base_url)
    new_data = response.json()
    reward_scale = new_data['data']['reward_scale']
    return reward_scale
 
def analyze_hotspot(hotspot, pagecount):
    tableList = []
    output={"data": []}    
    base_url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
    url = base_url
    # While loop to go thrrough the num of pages specified by the user and get all the data from the Helium api
    while pagecount:
        response = requests.get(url)
        new_data = response.json()
        output['data'].extend(new_data['data']) 
        cursor=new_data['cursor']
        url=base_url+'?cursor='+cursor
        pagecount -= 1
    
        # For loop to parse the data coming from the json file
    for i in output['data']:
        if (i['type'] == "poc_receipts_v1") and (i['path'][0]['challengee'] != hotspot):
            timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d-%I:%M:%S")
            challengee = i['path'][0]['challengee']
            # Get the reward scale of the challengee
            reward_scale = get_reward_scale(challengee)
            street = i['path'][0]['geocode']['short_street']
            city = i['path'][0]['geocode']['short_city']
            witnesses = len(i['path'][0]['witnesses'])
            
            # Create a dict of the data
            if(witnesses != 0):
                alltheData = {
                    'TimeStamp' : timestamp,
                    'Challengee' : challengee,
                    'reward_scale': reward_scale,
                    'Street'    : street,
                    'City'      : city,
                    'Witnesses' : witnesses
                }
                # Append all of it to the tableList
                tableList.append(alltheData)
    return tableList



        
        
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
    onetofive = occurOne + occurTwo + occurThree + occurFour + occurFive

    print(
        "1 Witnesses : ", occurOne,"times\n" 
        "2 Witnesses : ", occurTwo,"times\n"
        "3 Witnesses : ", occurThree,"times\n"
        "4 Witnesses : ", occurFour,"times\n"
        "5 Witnesses : ", occurFive,"times\n"
        "More than 5 Witnesses :", occurMore, "times\n"
        "Total Witnesses from 1-5 : ", onetofive, "times\n"
        "Total Witnesses : ", onetofive + occurMore, "\n\n"
        )
    # Detailed summary 
    new_col_list = ["Challengee"]
    df2 = pd.read_csv(file, usecols=new_col_list)
    Challengee = df2
    
    # print(
    #     "========================= Names of the Hotspots =========================\n "
    #     "Rounters with 1 witnesses :\n", remove_dup(Challengee[0:occurOne].values), "\n"
    #     "Rounters with 2 witnesses :\n", remove_dup(Challengee[occurOne:occurOne+occurTwo].values), "\n",
    #     "Rounter with 3 witnesses :\n", remove_dup(Challengee[occurOne+occurTwo:occurOne+occurTwo+occurThree].values), "\n",
    #     "Rounter with 4 witnesses :\n", remove_dup(Challengee[occurOne+occurTwo+occurThree:occurOne+occurTwo+occurThree+occurFour].values), "\n",
    #     "Rounter with 5 witnesses :\n", remove_dup(Challengee[occurOne+occurTwo+occurThree+occurFour:occurOne+occurTwo+occurThree+occurFour+occurFive].values), "\n"
    # )

def remove_dup(x):
    tuple_line = [tuple(pt) for pt in x]                            # convert list of list into list of tuple
    tuple_new_line = sorted(set(tuple_line),key=tuple_line.index)   # remove duplicated element
    new_line = [list(t) for t in tuple_new_line]                    # convert list of tuple into list of list
    return new_line

def sortCSV(file):
    # after the file is written we need to sort the csv file using pandas library 
    df = pd.read_csv(file)
    sorted_df = df.sort_values(by=["Witnesses"], ascending=True)
    sorted_df.to_csv('Sorted_hotspotData.csv', index=False)

        
hotspots = [#'112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg',
            #'112Cggcbje3yS4a1YpfyVNt1B2DTYNqiFjwaNEvfJp6fhc8UPuLc',
            #'112SDjb928fBrnhzLLLif1ZNowE9E8VYfkHLoQTUoUQtuijpaPVd',
            # '112na4aZ1XZsFFtAwUxtEfvn1kkP37yQ8zaTVvYBBEfkMEUkyzhx',
            
            # '11H8cjxUtx9WzCxPkbVq3AKzSYh7Wo5yWnPXLrf8eygiKt6hHVP',
            # '11c4pxUfwby5rtz2PtRm4oxmndc8WAcQg5BxT7CNpU56hHqvp9h',
            # '112KHUoQtauKc7hx2yDceHV1Q2X9DsCtdMeoK28gZMPJvHHLrAQz',
            '111MtVFr98Qs7Bs1u6CaVQFF2CjqJ83sLfxP1BPsAyR5h4Qa77A'
            
            ]

pageNum = int(input("Enter the page amount to check : "))
for i in range(len(hotspots)):
    data = analyze_hotspot(hotspots[i], pageNum)
    df = pd.DataFrame(data)
    df.to_csv('hotspotData.csv')
    #reward_scale('hotspotData.csv')
    sortCSV('hotspotData.csv')
    summary('Sorted_hotspotData.csv')

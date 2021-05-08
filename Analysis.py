# TODO
# Remove the entire record if the own hotspot was an invalid witness
# Remove the witness if it's marked invalid
# Add an option to define how many pages to traverse/download
# Move the page traversal/download into a function that runs through a loop and appends all the data into one json object
# Prepare a summary and a detailed view
# Load the list of hotspots from a file

# Imports
import requests
import json
from datetime import datetime
from beeprint import pp
import pandas as pd
import csv
import numpy as np

def analyze_hotspot(hotspot, pagecount):
    
    output={"data": []}    
    base_url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
    url = base_url
    tableList = []
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
            street = i['path'][0]['geocode']['short_street']
            city = i['path'][0]['geocode']['short_city']
            witnesses = len(i['path'][0]['witnesses'])
                # Create a dict of the data
            if(witnesses != 0):
                alltheData = {
                    'TimeStamp' : timestamp,
                    'Challengee' : challengee,
                    'Street'    : street,
                    'City'      : city,
                    'Witnesses' : witnesses
                }
                    # Append all of it to the tableList
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
        "More than 5 Witnesses :", occurMore, "times\n"
        )
    
    new_col_list = ["Challengee"]
    df2 = pd.read_csv(file, usecols=new_col_list)
    Challengee = df2
    # This prints the rounter when we are the only one witnessing 
    usersDf = pd.read_csv(file,  skipfooter= numLines-occurOne, usecols = new_col_list, engine='python')
    remove_dup = np.unique(usersDf).tolist()    # Removes the duplicates
    print(
        "Rounter with 1 witnesses :\n", remove_dup, "\n",
        "Rounters with 1 witnesses :\n", Challengee[0:occurOne].values, "\n",
        "Rounters with 2 witnesses :\n", Challengee[occurOne:occurOne+occurTwo].values, "\n",
        "Rounter with 3 witnesses :\n", Challengee[occurOne+occurTwo:occurOne+occurTwo+occurThree].values, "\n",
        "Rounter with 4 witnesses :\n", Challengee[occurOne+occurTwo+occurThree:occurOne+occurTwo+occurThree+occurFour].values, "\n",
        "Rounter with 5 witnesses :\n", Challengee[occurOne+occurTwo+occurThree+occurFour:occurOne+occurTwo+occurThree+occurFour+occurFive].values
    )

        
hs_mg='112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg'
hs_ag='112Cggcbje3yS4a1YpfyVNt1B2DTYNqiFjwaNEvfJp6fhc8UPuLc'
hs_jh='112SDjb928fBrnhzLLLif1ZNowE9E8VYfkHLoQTUoUQtuijpaPVd'
hs_jc='112na4aZ1XZsFFtAwUxtEfvn1kkP37yQ8zaTVvYBBEfkMEUkyzhx'

print("==================== "+"Clever Ivory Raccoon"+ " =====================\n")
data = analyze_hotspot(hs_mg, 4)
df = pd.DataFrame(data)
df.to_csv('hotspotData.csv')
sortCSV('hotspotData.csv')
summary('Sorted_hotspotData.csv')
print ("==================== "+ "Brilliant Latte Bear" + "===================\n")
data = analyze_hotspot(hs_ag, 4)
df = pd.DataFrame(data)
df.to_csv('hotspotData.csv')
sortCSV('hotspotData.csv')
summary('Sorted_hotspotData.csv')
print ("==================== "+ "Silly Aqua Carp" + "=========================\n")
data = analyze_hotspot(hs_jh, 4)
df = pd.DataFrame(data)
df.to_csv('hotspotData.csv')
sortCSV('hotspotData.csv')
summary('Sorted_hotspotData.csv')
print ("==================== "+ "Fluffy Taupe Aphid" + "======================\n")
data = analyze_hotspot(hs_jc, 4)
df = pd.DataFrame(data)
df.to_csv('hotspotData.csv')
sortCSV('hotspotData.csv')
summary('Sorted_hotspotData.csv')
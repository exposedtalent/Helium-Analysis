# TODO
# Remove the entire record if the own hotspot was an invalid witness
# Remove the witness if it's marked invalid
# Load the list of hotspots from a file

# Imports
import requests
from datetime import datetime
import pandas as pd
import numpy as np

# Function to get the reward scale of each of the challengee of the witnesses
def get_reward_scale(challengee):
    base_url='https://api.helium.io/v1/hotspots/' + challengee
    response = requests.get(base_url)
    new_data = response.json()
    reward_scale = new_data['data']['reward_scale']
    return reward_scale

# Function to analyzer the data from the activity tab of the Helium API 
def analyze_hotspot(hotspot, pagecount, rewardScale):
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
            if rewardScale:
                reward_scale = get_reward_scale(challengee)
            street = i['path'][0]['geocode']['short_street']
            city = i['path'][0]['geocode']['short_city']
            witnesses = len(i['path'][0]['witnesses'])
            
            # Create a dict of the data
            if(witnesses != 0 and rewardScale):
                alltheData = {
                    'TimeStamp' : timestamp,
                    'Challengee' : challengee,
                    'reward_scale': reward_scale,
                    'Street'    : street,
                    'City'      : city,
                    'Witnesses' : witnesses
                }
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

# Function for to print the small and detailed summary of the parsed data 
def summary(file,rewardScale):
    # Looks at only the Witnesses col and prints the num of Witnesses 
    col_list = ["Witnesses"]
    df = pd.read_csv(file, usecols=col_list)
    data = df.values
    
    if rewardScale:
        # Looks at only the Reward Scale col and store it in a list
        col_list2 = ["reward_scale"]
        df2 = pd.read_csv(file, usecols=col_list2)
        rewardScale = df2.values
        rs = list(np.concatenate(rewardScale).flat)
        
    # Looks at only the Challengee col and store it in a list
    new_col3 = ["Challengee"]
    df3 = pd.read_csv(file, usecols=new_col3)
    Challengee = df3

    # using the numpy lib we find the number of times this router has seen 1,2,3,4,5 or more witnesses for a challenge
    occurOne = np.count_nonzero(data == 1)  
    occurTwo = np.count_nonzero(data == 2)
    occurThree = np.count_nonzero(data == 3)
    occurFour = np.count_nonzero(data == 4)
    occurMore = np.count_nonzero(data >= 5)
    onetofour = occurOne + occurTwo + occurThree + occurFour 
    if rewardScale:
        print(
            "============= Witnesses =============\n"
            " 1 Witnesses : ", occurOne, "\tAVG Reward Scale :", round(avg(rs[0:occurOne]),3),"\n", 
            "2 Witnesses : ", occurTwo, "\tAVG Reward Scale :", round(avg(rs[occurOne:occurOne+occurTwo]),3),"\n",
            "3 Witnesses : ", occurThree, "\tAVG Reward Scale :", round(avg(rs[occurOne+occurTwo:occurOne+occurTwo+occurThree]),3),"\n",
            "4 Witnesses : ", occurFour, "\tAVG Reward Scale :", round(avg(rs[occurOne+occurTwo+occurThree:occurOne+occurTwo+occurThree+occurFour]),3),"\n",
            "More than 5 Witnesses :", occurMore, "\n\n",
            "Total Witnesses from 1-4 : ", onetofour, "\n",
            "Total Witnesses : ", onetofour + occurMore, "\n",
            )
    else :
        print(
            "============= Witnesses =============\n"
            " 1 Witnesses : ", occurOne,"\n", 
            "2 Witnesses : ", occurTwo, "\n",
            "3 Witnesses : ", occurThree, "\n",
            "4 Witnesses : ", occurFour, "\n",
            "More than 5 Witnesses :", occurMore, "\n\n",
            "Total Witnesses from 1-4 : ", onetofour, "\n",
            "Total Witnesses : ", onetofour + occurMore, "\n",
            )
    
    print(
        "========================= Names of the Hotspots =========================\n "
        "Rounters with 1 witnesses :\n", remove_dup(Challengee[0:occurOne].values), "\n\n"
        "Rounters with 2 witnesses :\n", remove_dup(Challengee[occurOne:occurOne+occurTwo].values), "\n\n",
        "Rounter with 3 witnesses :\n", remove_dup(Challengee[occurOne+occurTwo:occurOne+occurTwo+occurThree].values), "\n\n",
        "Rounter with 4 witnesses :\n", remove_dup(Challengee[occurOne+occurTwo+occurThree:occurOne+occurTwo+occurThree+occurFour].values), "\n\n\n",
    )

# Function to remove the duplicates in the hotspots name 
def remove_dup(x):
    tuple_line = [tuple(pt) for pt in x]                            # convert list of list into list of tuple
    tuple_new_line = sorted(set(tuple_line),key=tuple_line.index)   # remove duplicated element
    new_line = [list(t) for t in tuple_new_line]                    # convert list of tuple into list of list
    return new_line

# Function to sort the CSV file to be asending order for the # of Witnesses
def sortCSV(file):
    # after the file is written we need to sort the csv file using pandas library 
    df = pd.read_csv(file)
    sorted_df = df.sort_values(by=["Witnesses"], ascending=True)
    sorted_df.to_csv('Sorted_hotspotData.csv', index=False)

# Function to return avg of the list   
def avg(rs):
    return sum(rs) / len(rs)

def main():
    # List of the hotspots names       
    hotspots = [
                '112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg',
                # '112Cggcbje3yS4a1YpfyVNt1B2DTYNqiFjwaNEvfJp6fhc8UPuLc',
                # '112SDjb928fBrnhzLLLif1ZNowE9E8VYfkHLoQTUoUQtuijpaPVd',
                #'112na4aZ1XZsFFtAwUxtEfvn1kkP37yQ8zaTVvYBBEfkMEUkyzhx',
                
                # '11H8cjxUtx9WzCxPkbVq3AKzSYh7Wo5yWnPXLrf8eygiKt6hHVP',
                # '11c4pxUfwby5rtz2PtRm4oxmndc8WAcQg5BxT7CNpU56hHqvp9h',
                # '112KHUoQtauKc7hx2yDceHV1Q2X9DsCtdMeoK28gZMPJvHHLrAQz',
                # '111MtVFr98Qs7Bs1u6CaVQFF2CjqJ83sLfxP1BPsAyR5h4Qa77A'
                '112YWEDhqBGDwnVsuCujvA8sg1cxTL4g9jZAY7PbTii7YPZcyNDm'
                
                ]
    # This is the main program
    pageNum = int(input("Enter the page amount to check : "))
    # Turn True for for to print the avg reward scale 
    # WARNING : ADDS A LOT MORE TIME TO EXECUTE
    rewardScale = False
    for i in range(len(hotspots)):
        data = analyze_hotspot(hotspots[i], pageNum, rewardScale)
        df = pd.DataFrame(data)
        df.to_csv('hotspotData.csv')
        sortCSV('hotspotData.csv')
        summary('Sorted_hotspotData.csv', rewardScale)

if __name__ == "__main__":
    main()

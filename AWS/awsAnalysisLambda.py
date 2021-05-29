from datetime import datetime
import pandas as pd
import numpy as np
import json
import boto3
import requests

def lambda_handler(event, context):
    # gets the uri from the url
    hotspots = []
    path = event['path']
    x = path.split("/")
    hotspots.append(x[2])

    # This is the main program
    pageNum = 2
    # Turn True for for to print the avg reward scale 
    # WARNING : ADDS A LOT MORE TIME TO EXECUTE
    rewardScale = False
    
    data = analyze_hotspot(hotspots[0], pageNum, rewardScale)
    df = pd.DataFrame(data)
    to_csv(df.to_csv())
    sortCSV('s3://helium-analysis-data/hotspotData.csv')
    analysis = summary('s3://helium-analysis-data/Sorted_hotspotData.csv', rewardScale)
    jsonList = json.dumps(analysis, indent = 4)
    return{
        'statusCode' : 200,
        'body': jsonList
    }
    
def to_csv(data):
    count = 0 
    if count == 0:
        bucket_name = "helium-analysis-data"
        file_name = "hotspotData" + ".csv"
        s3_path = file_name
    
        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=data)
        count += 1
    if count == 1:
        bucket_name = "helium-analysis-data"
        file_name = "Sorted_hotspotData" + ".csv"
        s3_path = file_name
        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=data)

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

def summary(file,rewardScale):
    finalDict = {}
    hotspotNameDict = {}
    witnesseDict = {}
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
        witnesseDict = {
            "1_Wtinesses" : occurOne,
            "2_Wtinesses" : occurTwo,
            "3_Wtinesses" : occurThree,
            "4_Wtinesses" : occurFour,
            "5_Witneeses_And_Up" : occurMore,
            "Total_Witnesses_from_1-4" : onetofour, 
            "Total_Witnesses" : onetofour + occurMore
            
        }
    hotspotNameDict = {
        "Hotspots_with_1_Witnesses" : remove_dup(Challengee[0:occurOne].values), 
        "Hotspots_with_2_Witnesses" : remove_dup(Challengee[occurOne:occurOne+occurTwo].values),
        "Hotspots_with_3_Witnesses" : remove_dup(Challengee[occurOne+occurTwo:occurOne+occurTwo+occurThree].values), 
        "Hotspots_with_4_Witnesses" : remove_dup(Challengee[occurOne+occurTwo+occurThree:occurOne+occurTwo+occurThree+occurFour].values)
        
    }
    
    finalDict = {
        "Witnesses": witnesseDict,
        "HotspotName": hotspotNameDict
    }
    return finalDict

def remove_dup(x):
    tuple_line = [tuple(pt) for pt in x]                            # convert list of list into list of tuple
    tuple_new_line = sorted(set(tuple_line),key=tuple_line.index)   # remove duplicated element
    new_line = [list(t) for t in tuple_new_line]                    # convert list of tuple into list of list
    return new_line

def sortCSV(file):

    # after the file is written we need to sort the csv file using pandas library 
    df = pd.read_csv('s3://helium-analysis-data/hotspotData.csv')
    sorted_df = df.sort_values(by=["Witnesses"], ascending=True)
    to_csv(sorted_df.to_csv())


def avg(rs):
    return sum(rs) / len(rs)
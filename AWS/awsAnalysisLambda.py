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
    WitnesseshtmlList = """let array = %s;"""%analysis['Witnesses']
    hotspotName = """\nlet hotspotName = "%s";"""%hotspots[0]
    htmlTop = """
        <!DOCTYPE html>
        <html >
        <head>
        <meta charset="UTF-8">
        <title>Wifi Mist</title>
        
        <script src="https://s.codepen.io/assets/libs/modernizr.js" type="text/javascript"></scrip>
        <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
        <link rel="stylesheet" href= "https://heliumfrontend.s3.amazonaws.com/style.css">
        </head>
        
        <body style="background-color:lightblue;">
        <h1>Witnesses</h1>
        <div style="overflow-x:auto;">
        <table class="rwd-table">
        <tr>
        <th>Hotspot Name </th>
        <th>1 Witnesses</th>
        <th>2 Witnesses</th>
        <th>3 Witnesses</th>
        <th>4 Witnesses</th>
        <th>5 Witnesses and up</th>
        <th>Total Witnesses from 1-4</th>
        <th>Total Witnesses</th>
        </tr>
        <tbody id="myTable">
        
        </table>
        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script>
    """
    htmlBottom = """
        buildTable(array, hotspotName);
        
        function buildTable(data, hotspotName) {
            let table = document.getElementById("myTable");

            let row = `<tr>
                <td>${hotspotName}</td>
                <td>${data.Witnesses_1}</td>
                <td>${data.Witnesses_2}</td>
                <td>${data.Witnesses_3}</td>
                <td>${data.Witnesses_4}</td>
                <td>${data.Witnesses_5_and_up}</td>
                <td>${data.Total_Witnesses_from_1_to_4}</td>
                <td>${data.Total_Witnesses}</td>
            </tr>`;
            table.innerHTML += row;
    
        }
        </script>
        </body>
        </html>
    """
    
    finalhtml = htmlTop + WitnesseshtmlList + hotspotName + htmlBottom
    return{
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": finalhtml
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
            "Witnesses_1" : occurOne,
            "Witnesses_2" : occurTwo,
            "Witnesses_3" : occurThree,
            "Witnesses_4" : occurFour,
            "Witnesses_5_and_up" : occurMore,
            "Total_Witnesses_from_1_to_4" : onetofour, 
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



import requests
import pandas as pd
import numpy as np
import json
from botocore.exceptions import ClientError
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    
    # This is for getting the Hotspot Addr from the csv file
    col_list = ["Hotspot Addr"]
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

    # This is for getting the Hotspot Addr from the csv file
    col_list = ["Account Addr"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    accAddr = list(np.concatenate(data).flat)
    
    putData(addr, hostName, hotspotName, accAddr)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully added to database')
    }
def putData(addr, hostName, hotspotName, accAddr):
    for i in range(len(addr)):
        table.put_item(
            Item = {
                "HostName": hostName[i],
                "HotspotAddr": addr[i],
                "HotspotName": hotspotName[i],
                "AccountAddr": accAddr[i],
            }    
        )
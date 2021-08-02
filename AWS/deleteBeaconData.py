import json
import boto3
from datetime import date, timedelta
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    
    todayDate = date.today()
    td = timedelta(2)
    d = todayDate - td
    lowerDate = '%s'%d

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HotspotBeacons')

    response = table.scan(
        FilterExpression = Attr('BeaconTime').lt(lowerDate)
    )
    
    for i in response['Items']:
        cleanupTable = boto3.client('dynamodb').batch_write_item(
            RequestItems={
                'HotspotBeacons': [
                    {
                        'DeleteRequest': {
                            'Key': {
                                'Hotspot': { 'S': i['Hotspot'] },
                                'BeaconTime': { 'S': i['BeaconTime'] }
                            }
                        }
                    }
                ]
            }
        )
    
    return {
        'statusCode': 200,
        'body': 'Successfullly removed the items from Hotspot beacon and witnesses table'
    }

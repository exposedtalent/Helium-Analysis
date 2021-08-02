# import json
import boto3
from datetime import date, timedelta
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    
    todayDate = date.today()
    td = timedelta(2)
    d = todayDate - td
    lowerDate = '%s'%d

    dynamodb = boto3.resource('dynamodb')
    table1 = dynamodb.Table('HotspotWitnesses')
    
    res = table1.scan(
        FilterExpression = Attr('WitnesseTime').lt(lowerDate)
    )
    
    for i in res['Items']:
        cleanupTable = boto3.client('dynamodb').batch_write_item(
            RequestItems={
                'HotspotWitnesses': [
                    {
                        'DeleteRequest': {
                            'Key': {
                                'Hotspot': { 'S': i['Hotspot'] },
                                'WitnesseTime': { 'S': i['WitnesseTime'] }
                            }
                        }
                    }
                ]
            }
        )
   
    return {
        'statusCode': 200,
        'body': 'Successfully removed the items from Hotspot beacon and witnesses table'
    }


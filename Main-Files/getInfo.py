import json
import boto3
from boto3.dynamodb.conditions import Key, And, Attr, Between


def main():
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table("test")
 
    response = table.query(
       FilterExpression= Attr("Witnesses").between(1,5),
       KeyConditionExpression=Key('Hotspot').eq('112Cggcbje3yS4a1YpfyVNt1B2DTYNqiFjwaNEvfJp6fhc8UPuLc') & Key('WitnesseTime').between('2021-06-18', '2021-06-20')
    )
   
    

    print(response['Items'])
if __name__ == "__main__":
    main()

import boto3
import pandas as pd
import numpy as np
import requests
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    col_list = ["Hotspot Addr"]
    df = pd.read_csv("HeliumData.csv", usecols=col_list)
    values = df.values
    hotspot = list(np.concatenate(values).flat)
    

    for i in range(len(hotspot)):
        # Check if the hotspot is syncing  
        url='https://api.helium.io/v1/hotspots/' + hotspot[i]
        
        response = requests.get(url)
        new_data = response.json()
        height = new_data['data']['status']['height']
        block = new_data['data']['block']
        if(height == None or (block - height) >= 350):
            dif = block - height
            sendEmail(hotspot[i])

    return{
        "statusCode": 200,
        "body": "Hello"
    }

def sendEmail(hotspot):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "tanishq.mor@gmail.com"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "tanishq.mor@gmail.com"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-2"
    
    # The subject line for the email.
    SUBJECT = "Helium Hotspot change of status"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Helium Hotspot change of status\r\n"
                 "This email is being sent because one of your hotspots status of %s has been changed to Sycing  "
                 "sent by AWS Lambda"%hotspot
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Helium Hotspot change of status</h1>
      <p>This email is being sent because one of your hotspots status of  %s has been changed to Sycing sent by AWS Lambda</p>
    </body>
    </html>
                """%hotspot           
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
        # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    

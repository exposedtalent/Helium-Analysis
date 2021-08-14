import json
import boto3
import requests

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table3 = dynamodb.Table("Users")
    response = table3.scan()
    heliumData = response['Items']
    # Calling the get_rewards and putting the data into reward list
    get_rewards(heliumData)
    
    result =  {
        'statusCode': 302,
        'headers': {
            'Location': 'LINK',
        }
    }
    
    return result
    
def putDataBalance(balanceDict):
    dynamodb = boto3.resource('dynamodb')
    table2 = dynamodb.Table('HotspotRewardDict')  
    table2.put_item(
        Item = {
            'Name':'wifimist',
            'HNT_Price': str(balanceDict['HNT_Price']),
            'Hotspots_24H_HNT' : str(balanceDict['Hotspots_24H_HNT']),
            'Hotspots_24H_USD' : str(balanceDict['Hotspots_24H_USD']),
            'Hotspots_30D_HNT' : str(balanceDict['Hotspots_30D_HNT']),
            'Hotspots_30D_USD' : str(balanceDict['Hotspots_30D_USD']),
            'Total_HNT' : str(balanceDict['Total_HNT']),
            'Total_USD' : str(balanceDict['Total_USD']),
        }    
    )
# Function to get the reward summary of the given hotspots
def get_rewards(heliumData):
    # This is to figure out the time
    twentyfourHour = '-2%20day'
    thirtyDays = '-30%20day'
    # initlize the various lists
    total24hrs = []
    total30days = []
    balanceList = []
    wifimistSub24hrs = []
    wifimistSub30day = []
    wifimistSubbal = []
    
    # Binance API to get the current rate
    url='https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])
    try : 
        # for loop to calculate the rewards and the acc
        for i  in range(len(heliumData)):
            url='https://api.helium.io/v1/hotspots/' + heliumData[i]['HotspotAddr'] 
            response = requests.get(url)
            new_data = response.json()
            height = new_data['data']['status']['height']
            
            if(height != None):
                # URL for the 24 hours
                url='https://api.helium.io/v1/hotspots/' + heliumData[i]['HotspotAddr'] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
                response = requests.get(url)
                new_data = response.json()
                reward24hrs = new_data['data'][0]['total']
                total24hrs.append(reward24hrs)
                
                # URL for the 30 days 
                url='https://api.helium.io/v1/hotspots/' + heliumData[i]['HotspotAddr'] + '/rewards/sum?min_time=' + thirtyDays
                response = requests.get(url)
                new_data = response.json()
                reward30days = new_data['data']['total']
                total30days.append(reward30days)
                
                # To get the account balance of the users
                url='https://api.helium.io/v1/accounts/' + heliumData[i]['AccountAddr'] + '/stats'
                response = requests.get(url)
                new_data = response.json()
                data = new_data['data']['last_day'][0]['balance']
                if(data == None):
                    balance = 0
                else:
                    balance = data
                # If statement for personal Hotspots to ignore. Please get the hotspot address to exclude from the main table
                if (heliumData[i]['HotspotAddr'] == '112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg' or heliumData[i]['HotspotAddr'] == '112Cggcbje3yS4a1YpfyVNt1B2DTYNqiFjwaNEvfJp6fhc8UPuLc' or heliumData[i]['HotspotAddr'] == '11nBh4xnmAqQzgmmeV5ZtELr7oWR5g1oPS6Q5aCaVjU81D6eSC2'):
                    wifimistSub24hrs.append(reward24hrs)
                    wifimistSub30day.append(reward30days)
                    wifimistSubbal.append(balance)
                balanceList.append(balance)
            else:
                total24hrs.append(0)
                total30days.append(0)
                balanceList.append(0)
    except KeyError:
        print(KeyError)
            
    # Calculations
    subBal = sum(wifimistSubbal) / 100000000
    bal = sum(balanceList) / 100000000
    usdBal = (bal - subBal) * price
    
    balanceDict = {
        'HNT_Price': round(price, 2),
        'Hotspots_24H_HNT' : round(sum(total24hrs) - sum(wifimistSub24hrs), 2),
        'Hotspots_24H_USD' : round((sum(total24hrs)  - sum(wifimistSub24hrs)) * price, 2),
        'Hotspots_30D_HNT' : round(sum(total30days) - sum(wifimistSub30day), 2),
        'Hotspots_30D_USD' : round((sum(total30days) - sum(wifimistSub30day)) * price, 2),
        'Total_HNT' : round(bal - subBal , 2),
        'Total_USD' : round(usdBal, 2),
        
    }
    putDataBalance(balanceDict)


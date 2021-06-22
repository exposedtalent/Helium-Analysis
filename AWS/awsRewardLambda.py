import requests
import pandas as pd
import numpy as np
import json
from botocore.exceptions import ClientError
import boto3
rewardList = None


def lambda_handler(event, context):
    # This is to figure out the time
    twentyfourHour = '-2%20day'
    thirtyDays = '-30%20day'

    # This is for getting the Hotspot Addr fromt the csv file
    col_list = ["Hopstop Addr"]
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

    # This is for getting the Hotspot Addr fromt the csv file
    col_list = ["Account Addr"]
    df = pd.read_csv('HeliumData.csv', usecols=col_list)
    data = df.values
    accAddr = list(np.concatenate(data).flat)
    # Calling the get_rewards and putting the data into reward list
    rewardsList = get_rewards(addr, twentyfourHour,thirtyDays, hostName, hotspotName, accAddr)
    
    # Dynamically adding data from the varibles into a string used for js script
    balanceHtmlDict = """let dict = %s"""%rewardsList['Balance']
    # Dynamically adding data from the varibles into a string used for js script
    hotspotsHtmlList = """\nlet array = %s"""%rewardsList['Hotspots']

    # Top half of the html with inline css code. This creates a table and style it using css
    topHtml = """<!DOCTYPE html><html ><head>
      <meta charset="UTF-8">
      <title>Wifi Mist</title>
          <script src="https://code.jquery.com/jquery-1.11.0.min.js"></script>

      <script src="https://s.codepen.io/assets/libs/modernizr.js" type="text/javascript"></scrip>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
      <link rel="stylesheet" href= "https://heliumfrontend.s3.amazonaws.com/style.css">

    </head>
    
    <body style="background-color:white;">
      <h1>Balance</h1>
     <div style="overflow-x:auto;">
    <table class="rwd-table">
      <tr>
        <th>HNT Price</th>
        <th>Hotspot 24H HNT</th>
        <th>Hotspot 24H USD</th>
        <th >Hotspot 30D HNT</th>
        <th >Hotspot 30D USD</th>
        <th >Total HNT</th>
        <th >Total USD</th>
      </tr>
      <tbody id="myBalTable">
      
    </table>
    </div>
    <h1>Hotspots Information</h1>
    <div style="overflow-x:auto;">
    <table class="rwd-table">
    
        <th data-column='HotspotOwner' data-order='desc'>Hotspot Owner &#9650</th>
        <th data-column='HotspotAddress' data-order='desc'>Hotspot Address &#9650</th>
        <th data-column='HotspotName' data-order='desc'>Hotspot Name &#9650</th>
        <th data-column='Hotspot24HHNT' data-order='desc'>Hotspot 24H HNT &#9650</th>
        <th data-column='Hotspot24HUSD' data-order='desc'>Hotspot 24H USD &#9650</th>
        <th data-column='Change' data-order='desc'>24H Change &#9650</th>
        <th data-column='Synced Status' data-order='desc'>Synced Status &#9650</th>
        <th data-column='Hotspot30DHNT' data-order='desc'>Hotspot 30D HNT &#9650</th>
        <th data-column='Hotspot30DUSD' data-order='desc'>Hotspot 30D USD &#9650</th>
        <th data-column='WalletBalance' data-order='desc'>Wallet Balance &#9650</th>
        <th data-column='WalletBalanceUSD' data-order='desc'>Wallet Balance USD &#9650</th>
        </tr>
    
      <tbody id="myTable">
     </table>
    </div>
        <script>
    """
    # This is the bottom of the html with js script inline
    bottomHtml = """
    $('th').on('click', function(){
                var column = $(this).data('column')
                var order = $(this).data('order')
                console.log('Col in the function', column, order)
            
                if(order == 'desc'){
                    $(this).data('order', "asc")
                    array = array.sort((a,b) => a[column] > b[column]? 1 : -1)   
                }
                else{
                    $(this).data('order', "asc")
                    array = array.sort((a,b) => a[column] < b[column]? 1 : -1)
                }
                buildTable(array)
            
            })
     $(document.body).on("click", "td[data-href]", function (){
            $(this).text();
            window.location.href = this.dataset.href
        })
    buildTable(array)
    buildBalTable(dict)
    
    
    function buildBalTable(data){
        let table = document.getElementById("myBalTable")
        let row = `<tr>
            <td>${data.HNT_Price}</td>
            <td>${data.Hotspots_24H_HNT}</td>
            <td>${data.Hotspots_24H_USD}</td>
            <td>${data.Hotspots_30D_HNT}</td>
            <td>${data.Hotspots_30D_USD}</td>
            <td>${data.Total_HNT}</td>
            <td>${data.Total_USD}</td>
         </tr>`
        table.innerHTML += row
    
    }
    
    function buildTable(data) {
    let table = document.getElementById("myTable");
    table.innerHTML = "";
    base_url = "https://gfz4azqik2.execute-api.us-east-2.amazonaws.com/default/invoke-HeliumRewards/";
    console.log(base_url)
    for (let i = 0; i < data.length; i++) {
        let syncedColor;
        let changeColor;
        if (data[i].Synced_Status == "Synced") {
            syncedColor = 'lightgreen';
        } else {
            syncedColor = 'red';
        }
        if (data[i].Change_24H >= 0) {
            changeColor = 'lightgreen';
        } else {
            changeColor = 'red';
        }

        let row = `<tr>
            <td>${data[i].Hotspot_Owner}</td>
            <td data-href="${base_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Address}</td>
            <td>${data[i].Hotspot_Name}</td>
            <td>${data[i].Hotspot_24H_HNT}</td>
            <td>${data[i].Hotspot_24H_USD}</td>
            <td style="color :${changeColor}">${data[i].Change_24H}</td>
            <td style="color :${syncedColor} ">${data[i].Synced_Status}</td>
            <td>${data[i].Hotspot_30D_HNT}</td>
            <td>${data[i].Hotspot_30D_USD}</td>
            <td>${data[i].Wallet_Balance}</td>
            <td>${data[i].Wallet_Balance_USD}</td>
        </tr>`;
        table.innerHTML += row;
        }
    }
      </script>
    
    
    </body>
    </html>
    """
    # Finally put together the differernt html strings into one to be returned
    finalHtml = topHtml + balanceHtmlDict + hotspotsHtmlList + bottomHtml

    # returns the final html string and that is run on the client side
    return{
        # "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": finalHtml
    }


# Function to get the reward summary of the given hotspots
def get_rewards(hotspot, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr):
    # initlize the various lists
    rewardList = []
    total24hrs = []
    total30days = []
    rewardChange = []
    syncStatus = []
    balanceList = []
    
    # Binance API to get the current rate
    url='https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])
    
    
    # for loop to calculate the rewards and the acc
    
    for i  in range(len(hotspot)):
        # Check if the hotspot is syncing  
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] 
        response = requests.get(url)
        new_data = response.json()
        height = new_data['data']['status']['height']
        block = new_data['data']['block']
        if(height == None or (block - height) >= 250):
            syncStatus.append("Not Synced")
            sendEmail(hotspot[i])
        else:
            syncStatus.append("Synced")
        if(height != None  ):
            # URL for the 24 hours
            url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
            response = requests.get(url)
            new_data = response.json()
            reward24hrs = new_data['data'][0]['total']
            reward2day = new_data['data'][1]['total']

            if(reward24hrs == 0 and reward2day == 0):
                change = 0
            else:
                change = (round((reward24hrs - reward2day) / reward2day * 100, 2))
            rewardChange.append(change)
            total24hrs.append(reward24hrs)
            
            # URL for the 30 days 
            url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + thirtyDays
            response = requests.get(url)
            new_data = response.json()
            reward30days = new_data['data']['total']
            total30days.append(reward30days)
            
            # To get the account balance of the users
            url='https://api.helium.io/v1/accounts/' + accAddr[i] + '/stats'
            response = requests.get(url)
            new_data = response.json()
            balance = new_data['data']['last_day'][0]['balance']
            balanceList.append(balance)
            
            # Put eveything into a dict
            rewardDict = {
                'Hotspot_Owner' : hostName[i],
                'Hotspot_Address' : hotspot[i],
                'Hotspot_Name' : hotspotName[i],
                'Hotspot_24H_HNT' : round(total24hrs[i], 2),
                'Hotspot_24H_USD' : round(total24hrs[i] * price, 2),
                'Change_24H' : rewardChange[i],
                'Synced_Status': syncStatus[i],
                'Hotspot_30D_HNT' : round(total30days[i], 2),
                'Hotspot_30D_USD' : round(total30days[i] * price, 2),
                'Wallet_Balance' : round(balanceList[i] / 100000000 , 2),
                'Wallet_Balance_USD' : round((balanceList[i] / 100000000) * price , 2),
            
            }
            rewardList.append(rewardDict)
    # Calculations
    bal = sum(balanceList) / 100000000
    usdBal = bal * price
    
    balanceDict = {
        'HNT_Price': round(price, 2),
        'Hotspots_24H_HNT' : round(sum(total24hrs), 2),
        'Hotspots_24H_USD' : round(sum(total24hrs) * price, 2),
        'Hotspots_30D_HNT' : round(sum(total30days), 2),
        'Hotspots_30D_USD' : round(sum(total30days) * price, 2),
        'Total_HNT' : round(bal, 2),
        'Total_USD' : round(usdBal, 2),
        
    }
    dataDict = {
            'Balance' : balanceDict,
            'Hotspots' : rewardList,
            
        }
    
    return dataDict
    
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
    

import requests
import pandas as pd
import numpy as np
import json

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
      <script src="https://s.codepen.io/assets/libs/modernizr.js" type="text/javascript"></script>
      <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
      <link rel="stylesheet" href= "https://heliumfrontend.s3.amazonaws.com/style.css">
    <style>
    td[data-href]{
    cursor: pointer;
    }
    </style>
    </head>
    
    <body style="background-color:lightblue;">
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
    
    function buildTable(data){
        let table = document.getElementById("myTable")
        table.innerHTML = ""
        base_url = "https://gfz4azqik2.execute-api.us-east-2.amazonaws.com/default/invoke-HeliumRewards/";        
        for (let i = 0; i < data.length; i++){
            let row = `<tr>
                <td>${data[i].Hotspot_Owner}</td>
                <td data-href="${base_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Address}</td>
                <td>${data[i].Hotspot_Name}</td>
                <td>${data[i].Hotspot_24H_HNT}</td>
                <td>${data[i].Hotspot_24H_USD}</td>
                <td>${data[i].Change_24H}</td>
                <td>${data[i].Hotspot_30D_HNT}</td>
                <td>${data[i].Hotspot_30D_USD}</td>
                <td>${data[i].Wallet_Balance}</td>
                <td>${data[i].Wallet_Balance_USD}</td>
            </tr>`
            table.innerHTML += row
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
    balanceList = []

    # for loop for getting the reward summary from the Helium API
    for i in range(len(hotspot)):
        # URL for the 24 hours
        url = 'https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
        response = requests.get(url)
        new_data = response.json()
        reward24hrs = new_data['data'][0]['total']
        reward2day = new_data['data'][1]['total']
        change = (round((reward24hrs - reward2day) / reward2day * 100, 2))
        rewardChange.append(change)
        total24hrs.append(reward24hrs)

        # URL for the 30 days
        url = 'https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + thirtyDays
        response = requests.get(url)
        new_data = response.json()
        reward30days = new_data['data']['total']
        total30days.append(reward30days)

    # Binance API to get the current rate
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])

    # For loop to get the account balance of the user
    for i in range(len(accAddr)):
        url = 'https://api.helium.io/v1/accounts/' + accAddr[i] + '/stats'
        response = requests.get(url)
        new_data = response.json()
        balance = new_data['data']['last_day'][0]['balance']
        balanceList.append(balance)

    # Calculations
    bal = sum(balanceList) / 100000000
    usdBal = bal * price
    # Loop to get the data into a dict that is appened to a list
    for i in range(len(hotspot)):
        # Put eveything into a dict
        rewardDict = {
            'Hotspot_Owner': hostName[i],
            'Hotspot_Address': hotspot[i],
            'Hotspot_Name': hotspotName[i],
            'Hotspot_24H_HNT': round(total24hrs[i], 2),
            'Hotspot_24H_USD': round(total24hrs[i] * price, 2),
            'Change_24H': rewardChange[i],
            'Hotspot_30D_HNT': round(total30days[i], 2),
            'Hotspot_30D_USD': round(total30days[i] * price, 2),
            'Wallet_Balance': round(balanceList[i] / 100000000, 2),
            'Wallet_Balance_USD': round((balanceList[i] / 100000000) * price, 2),

        }
        rewardList.append(rewardDict)
    # Dict for the balance part of the json
    balanceDict = {
        'HNT_Price': round(price, 2),
        'Hotspots_24H_HNT': round(sum(total24hrs), 2),
        'Hotspots_24H_USD': round(sum(total24hrs) * price, 2),
        'Hotspots_30D_HNT': round(sum(total30days), 2),
        'Hotspots_30D_USD': round(sum(total30days) * price, 2),
        'Total_HNT': round(bal, 2),
        'Total_USD': round(usdBal, 2),

    }
    # Put the two different dicts into one big one for the json
    dataDict = {
        'Balance': balanceDict,
        'Hotspots': rewardList,

    }
    # return
    return dataDict

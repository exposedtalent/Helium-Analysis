import requests
import pandas as pd
import numpy as np
import json
import codecs

rewardList = []

def lambda_handler(event, context):
    bucket = 'heliumrewardsdata'
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
    
    rewardsList = get_rewards(addr, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr)
    # print(rewardsList['Hotspots'][0]['Hotspot_Address'])

    balanceHtmlDict = """
    let dict = {
        "HNT_Price":%s,
        "Hotspots_24H_HNT": %s,
        "Hotspots_24H_USD": %s,
        "Hotspots_30D_HNT": %s,
        "Hotspots_30D_USD": %s,
        "Total_HNT": %s,
        "Total_USD": %s}"""%(
            rewardsList['Balance']['HNT_Price'],
            rewardsList['Balance']['Hotspots_24H_HNT'],
            rewardsList['Balance']['Hotspots_24H_USD'],
            rewardsList['Balance']['Hotspots_30D_HNT'],
            rewardsList['Balance']['Hotspots_30D_USD'],
            rewardsList['Balance']['Total_HNT'],
            rewardsList['Balance']['Total_USD'],
                
    )
                
    
    temp = """"""
    for i in range(len(rewardsList['Hotspots'])):
        data = """ 
        {
            "Hotspot_Owner": "%s",
            "Hotspot_Address": "%s",
            "Hotspot_Name": "%s",
            "Hotspot_24H_HNT": %s,
            "Hotspot_24H_USD": %s,
            "Change_24H": %s,
            "Hotspot_30D_HNT": %s,
            "Hotspot_30D_USD": %s,
            "Wallet_Balance": %s,
            "Wallet_Balance_USD": %s
        },
        """%(
            rewardsList['Hotspots'][i]['Hotspot_Owner'],
            rewardsList['Hotspots'][i]['Hotspot_Address'],
            rewardsList['Hotspots'][i]['Hotspot_Name'],
            rewardsList['Hotspots'][i]['Hotspot_24H_HNT'],
            rewardsList['Hotspots'][i]['Hotspot_24H_USD'],
            rewardsList['Hotspots'][i]['Change_24H'],
            rewardsList['Hotspots'][i]['Hotspot_30D_HNT'],
            rewardsList['Hotspots'][i]['Hotspot_30D_USD'],
            rewardsList['Hotspots'][i]['Wallet_Balance'],
            rewardsList['Hotspots'][i]['Wallet_Balance_USD'],
        )
        temp += data
    hotspotsHtmlList = """\nlet array = [%s]"""%temp  

    # put the result into a json
    topHtml = """<!DOCTYPE html><html ><head>
      <meta charset="UTF-8">
      <title>Wifi Mist</title>
      <script src="https://s.codepen.io/assets/libs/modernizr.js" type="text/javascript"></script>
      <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
    
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
    <style type="text/css" media="screen">
    @import "https://fonts.googleapis.com/css?family=Montserrat:300,400,700";
    .rwd-table {
      margin: 1em 0;
      min-width: 300px;
    }
    .rwd-table tr {
      border-top: 1px solid #ddd;
      
      border-bottom: 1px solid #ddd;
    }
    .rwd-table th {
      display: none;
    }
    .rwd-table td {
      display: block;
    }
    .rwd-table td:first-child {
      padding-top: .5em;
    }
    .rwd-table td:last-child {
      padding-bottom: .5em;
    }
    .rwd-table td:before {
      content: attr(data-th) ": ";
      font-weight: bold;
      width: 6.5em;
      display: inline-block;
    }
    @media (min-width: 480px) {
      .rwd-table td:before {
        display: none;
      }
    }
    .rwd-table th, .rwd-table td {
      text-align: left;
    }
    @media (min-width: 480px) {
      .rwd-table th, .rwd-table td {
        display: table-cell;
        padding: .25em .5em;
      }
      .rwd-table th:first-child, .rwd-table td:first-child {
        padding-left: 0;
      }
      .rwd-table th:last-child, .rwd-table td:last-child {
        padding-right: 0;
      }
    }
    
    body {
      padding: 0 2em;
      font-family: Montserrat, sans-serif;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
      color: #444;
      background: #eee;
     
    }
    
    h1 {
      font-weight: normal;
      letter-spacing: -1px;
      color: #34495E;
    }
    
    .rwd-table {
      background: #34495E;
      color: #fff;
      border-radius: .4em;
      overflow: hidden;
    }
    .rwd-table tr {
      border-color: #46637f;
    }
    .rwd-table th, .rwd-table td {
      margin: .5em 1em;
    }
    @media (min-width: 480px) {
      .rwd-table th, .rwd-table td {
        padding: 1em !important;
      }
    }
    .rwd-table th, .rwd-table td:before {
      color: #dd5;
    }
    </style>
    
      
    </head>
    
    <body>
      <h1>Balance</h1>
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
    <h1>Hotspots Information</h1>
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
        <script>
    """
    
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
        for (let i = 0; i < data.length; i++){
            let row = `<tr>
                <td>${data[i].Hotspot_Owner}</td>
                <td>${data[i].Hotspot_Address}</td>
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
    
    </table>
    </body>
    </html>
    """
    finalHtml = topHtml + balanceHtmlDict + hotspotsHtmlList + bottomHtml
    
    # change to this for aws Lambda instead of print
    return{
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},   
        "body": finalHtml
    }
    
    

def get_rewards(hotspot, twentyfourHour, thirtyDays, hostName, hotspotName, accAddr):
    
    total24hrs = []
    total30days = []
    rewardChange = []
    
    for i in range(len(hotspot)):
        # URL for the 24 hours
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + twentyfourHour + '&bucket=day'
        response = requests.get(url)
        new_data = response.json()
        reward24hrs = new_data['data'][0]['total']
        reward2day = new_data['data'][1]['total']
        change = (round((reward2day - reward24hrs ) / reward2day * 100, 2))
        rewardChange.append(change)
        total24hrs.append(reward24hrs)
        
        # URL for the 30 days 
        url='https://api.helium.io/v1/hotspots/' + hotspot[i] + '/rewards/sum?min_time=' + thirtyDays
        response = requests.get(url)
        new_data = response.json()
        reward30days = new_data['data']['total']
        total30days.append(reward30days)

    
    # Append the dict into a list
    # Function to get tthe total balance of all accounts
    balanceList = []
    
    # Binance API to get the current rate
    url='https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    response = requests.get(url)
    new_data = response.json()
    price = float(new_data['price'])
    
    # For loop to get the account balance of the user
    for i in range(len(accAddr)):
        url='https://api.helium.io/v1/accounts/' + accAddr[i] + '/stats'
        response = requests.get(url)
        new_data = response.json()
        balance = new_data['data']['last_day'][0]['balance']
        balanceList.append(balance)
        
    # Calculations
    bal = sum(balanceList) / 100000000
    usdBal = bal * price
    for i in range(len(hotspot)):
        # Put eveything into a dict
        rewardDict = {
            'Hotspot_Owner' : hostName[i],
            'Hotspot_Address' : hotspot[i],
            'Hotspot_Name' : hotspotName[i],
            'Hotspot_24H_HNT' : round(total24hrs[i], 2),
            'Hotspot_24H_USD' : round(total24hrs[i] * price, 2),
            'Change_24H' : rewardChange[i],
            'Hotspot_30D_HNT' : round(total30days[i], 2),
            'Hotspot_30D_USD' : round(total30days[i] * price, 2),
            'Wallet_Balance' : round(balanceList[i] / 100000000 , 2),
            'Wallet_Balance_USD' : round((balanceList[i] / 100000000) * price , 2),
            
        }
        rewardList.append(rewardDict)
    
    balanceDict = {
        'HNT_Price' : round(price, 2),
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
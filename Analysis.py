import requests
from datetime import datetime
# Using this can change the network address
hotspot='112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg'
# Url for the helium api
url='https://api.helium.io/v1/hotspots/' + hotspot + '/activity'
# using the request library to get the data into a json
response = requests.get(url)
output = response.json()
# cursor needded to go to next pages 
cursor = output['cursor']
my_dict = {"Time":[],"Challenge":[],"Street":[],"City":[],"Witnesses":[]}
# for loop to go throught the first page and print the data 
for i in output['data']:
    if (i['type'] == "poc_receipts_v1"):
        timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
        challengee = i['path'][0]['challengee']
        street = i['path'][0]['geocode']['short_street']
        city = i['path'][0]['geocode']['short_city']
        witnesses = len(i['path'][0]['witnesses'])
        
        print(timestamp,"\t", challengee, "\t", street, city, witnesses)
        
        
# for loop to go thrught and print the data after using cursor to go to next page
url=url+'?cursor='+cursor
response = requests.get(url)
output = response.json()
for i in output['data']:
    if (i['type'] == "poc_receipts_v1"):
        timestamp = datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %I:%M:%S")
        challengee = i['path'][0]['challengee']
        street = i['path'][0]['geocode']['short_street']
        city = i['path'][0]['geocode']['short_city']
        witnesses = len(i['path'][0]['witnesses'])
        my_dict["Time"].append(timestamp)
        my_dict["Challenge"].append(challengee)
        my_dict["Street"].append(street)
        my_dict["City"].append(city)
        my_dict["Witnesses"].append(witnesses)
        
         
        # print(timestamp,"\t", challengee, "\t", street, city, witnesses)
        
print("Time :", my_dict['Time'])
print("Challenge : ", my_dict["Challenge"])
print("Street : ", my_dict["Street"])
print("City : ", my_dict["City"])
print("Witnesses : ", my_dict["Witnesses"])

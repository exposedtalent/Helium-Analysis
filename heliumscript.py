from helium import *
from bs4 import BeautifulSoup
import requests

start_chrome()
go_to('https://explorer.helium.com/hotspots/112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg')

# https://www.sitebot.com/helium/hotspot/clever-ivory-raccoon/challenges
# this is show all the challenges in the past 24 hours 
click('Activity')

#click('Export CSV')
for x in range (5):
    click('Expand row')
    wait_until(highlight("WITNESSES"))
    
    
    
click(Button('Load More'))    


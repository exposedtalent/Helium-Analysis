from bs4 import BeautifulSoup
import requests


source = requests.get('https://explorer.helium.com/hotspots/112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg').text
soup = BeautifulSoup(source, 'lxml')

mainTable = soup.find('main', class_='ant-layout-content')
mainCell = mainTable.find('div', class_='ant-row ant-row-center undefined')
thecell = mainCell.find('tbody', class_='ant-table-tbody')

print(mainCell)

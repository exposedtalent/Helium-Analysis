from bs4 import BeautifulSoup
import requests
list = []
list2 = []
counter = 0
source = requests.get('https://www.sitebot.com/helium/hotspot/clever-ivory-raccoon/challenges').text
soup = BeautifulSoup(source, 'lxml')
# Returns the whole query of an challenge with witnesses
wholes = soup.find_all('div', class_='card1 marb20 pad20 mobile-scrollx')
for whole in wholes :
# Returns the challenges name where iss signal wass started from
    challengeeTable = whole.find('table', class_ = 'marb20 table11 w100').text
    challengee = challengeeTable.find('a')
    list2.append(challengee)
# Returns the witnesses from the tables
    witnesses = whole.find_all('table', class_ ='table11 w100')
    for witness in witnesses:
# Returns the single witness
        singleWitness = witness.find('td').text
        counter+=1
        list.append(singleWitness)


# Returns the challengee
# test = important.find('td', class_ = 'nowrap')
print("Witnesses: ")
print(list)
print("Challenge: ")
print(list2)
print("The number of witnesse: ")
print(counter)





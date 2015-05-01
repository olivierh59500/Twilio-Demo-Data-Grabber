#!/usr/bin/python
import requests
import json
import sqlite3
from bs4 import BeautifulSoup
import urllib
'''
This program is a work in progress that automates carrier lookup information lookup from Twilio's demo website and
writes it into a database for later use. This program is for demonstration and education purposes only.

'''
 
#Create SQLite3 DB
db = sqlite3.connect('phones.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Twilio_Data
                (phone_number text, country_code text, carrier text, type text)''')

#Path to a list of Phone Numbers to Check. You Need to Change This Manually for Now.
numberList = open('/usr/share/wordlists/phones.txt', 'r').read().splitlines()


#These Headers Work. Change User-Agent if you feel like it.
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.6.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.twilio.com',
        'content-length': '158'}

#Grab A CSRF Token
r = requests.get('http://www.twilio.com/lookup')
soupedupText = BeautifulSoup(r.text)
csrfToken = soupedupText.find("meta",{"name" : "csrfToken"})['content']
csrfToken_Urlized = urllib.quote(csrfToken)
payload = 'CSRF=' + csrfToken_Urlized

for number in numberList:
        r = requests.post("http://www.twilio.com/functional-demos?Type=lookup&PhoneNumber=" + number, data=payload, headers=headers)
        print r.status_code
#        print r.text
        jsonData = json.loads(r.text)
#        print jsonData
        print json.dumps(jsonData, indent=3, sort_keys=True)
        carrierName = jsonData['body']['carrier']['name']
        countryCode = jsonData['body']['country_code']
	numberType = jsonData['body']['carrier']['type']
#        print countryCode
#        print carrierName
        cursor.execute(
            '''INSERT INTO Twilio_Data '''
            '''(phone_number, country_code, carrier, type)'''
            '''VALUES (?,?,?,?)''', (number, carrierName, countryCode, numberType))
        db.commit()

db.close()

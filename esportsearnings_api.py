# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:34:58 2017

@author: alexharmon
"""

import requests
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf8')

counter = 0
codedex1 = ''
apikey1 = 'apikey=YOUR_API_KEY_HERE’
game = '&gameid=351'
offsetlist=[]
for i in range(0,10000,100):
    offsetlist.append('&offset='+str(i)) 
format1 ='&format=csv'
base = 'http://api.esportsearnings.com/v0/LookupHighestEarningPlayersByGame?'
for offset in offsetlist:
    request = base+apikey1+game+offset+format1
    r = requests.get(request)
    if len(r.text)>0:
        codedex1 = codedex1+r.text[67:]
    if len(r.text) is 0:
        break
    counter += 1
    sleep(1)
    print('{} of (less than) {} complete!').format(counter,len(offsetlist))
codedex = 'PlayerId,NameFirst,NameLast,CurrentHandle,CountryCode,TotalUSDPrize'+codedex1
text_file = open("smite_players.csv", "w")
text_file.write(codedex)
text_file.close()
print('Write Success')

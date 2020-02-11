# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 11:59:44 2017

@author: alexharmon
"""
import csv
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import pandas as pd
from time import sleep
import random
reload(sys)
sys.setdefaultencoding('utf8')
tournamentlist =[]
tablerow =[]
tablerow.append('NameFirst,CurrentHandle, DateofBirth')
counter =0
base = 'https://www.esportsearnings.com/players/'
playerlist = []
df = pd.read_csv('Dota2_players.csv')
for player in (df['PlayerId']):
    playerlist.append(base+str(player))
random.shuffle(playerlist,random.random)
for playerpage in playerlist:
    singlerow =[]
    try:
        page=urllib2.urlopen(playerpage)
        soup = BeautifulSoup(page)
        info = soup.findAll('div', {'class':'detail_option_footer'})
        information = info[0].findAll('div', {'class':'format_cell info_text_value'})
        try:
            dob=information[1].text
        except:
            dob ='unknown'
        try:
            pagetitle = soup.find('h1', {'class' : 'info_box_title'}).text.split()
        except:
            firstname ='-'
            playerhandle= '-'
        try:        
            firstname = pagetitle[0]
        except:
            firstname ='-'
        try:
            playerhandle= pagetitle[1]
        except:
            playerhandle= '-'
        singlerow.append(firstname)
        singlerow.append(playerhandle)
        singlerow.append(dob)
        tablerow.append(singlerow)
    except:
        print(playerpage)
    counter +=1
    print('{} of {} complete!').format(counter,len(playerlist))
    sleepvalue = random.uniform(1.5, 3.0)
    sleep(sleepvalue)
with open('CSGO_DoB.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(tablerow)
print('File write success')

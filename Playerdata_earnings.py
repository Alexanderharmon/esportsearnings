# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 22:14:07 2017

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
#tablerow.append('playerhandle,playername,playercountry,date_of_birth,player_tournament_id,tournament_date,tournamnet_placement,tournament,tournament_url,tournament_date,teamsplit,prize,game')
counter =0
base = 'https://www.esportsearnings.com/players/'
base2 = 'https://www.esportsearnings.com'
playerlist = []
df = pd.read_csv('smite_players.csv')
for player in (df['PlayerId']):
    playerlist.append(base+str(player))
random.shuffle(playerlist,random.random)
for playerpage in playerlist:
    singlerow =[]   
    try:
    #if True is True:
        page=urllib2.urlopen(playerpage)
        soup = BeautifulSoup(page)
        try:
            goodinfo = soup.findAll('div', {'class':'detail_option_footer'})
            try:
                expanded = goodinfo[4].find('a')['href']
            except:
                expanded = goodinfo[3].find('a')['href']
            expandedpage = base2+str(expanded)
            #print(expandedpage)
            #goodinfo[4] is results by year. Change for different sorting
            expandedpage = urllib2.urlopen(expandedpage)
            expandedsoup = BeautifulSoup(expandedpage)
        except:
            pass
        infobox = expandedsoup.find('div', {'class':'info_box'})
        playerboxes = infobox.findAll('div', {'class':'info_box_inner'})
        namebox = playerboxes[0]
        rowes = namebox.findAll('div', {'class':'format_row'})        
        try:
            playername = rowes[0].find('div', {'class':'format_cell info_text_value'}).text
        except:
            playername = 'error'
        try:
            dob = rowes[1].find('div', {'class':'format_cell info_text_value'}).text
        except:
            dob = 'unknown'
        try:
            countrybox = playerboxes[1]
            country = countrybox.find('div', {'class':'info_country'})
            playercountry = (country.find('img')['title'])
        except:
            playercountry = 'error'
        try:
            pagetitle = expandedsoup.find('h1', {'class' : 'info_box_title'}).text.split()
        except:
            playerhandle= 'error'
        try:
            playerhandle= pagetitle[1]
        except:
            playerhandle= 'error'
        try:
            results = expandedsoup.find('table', {'class':'detail_list_table'})
        except:
            print('Build exception for a player with no results table')
        for row in results.findAll('tr'):
            try:
                ptournnumber = row.find('td', {'class' : 'format_cell detail_list_order'}).text
            except:
                ptournnumber = 'error'
            try:
                tournament_date = row.find('td', {'class' : 'detail_list_date'}).text
            except:
                tournament_date = 'error'
            try:
                placement = row.findAll('td')
                tournament_placement = placement[2].text
            except:
                tournament_placement = 'error'
            try:
                tournamentinfo = row.find('td', {'class' : 'detail_list_tournament earning_note_box'})
            except:
                continue
            try:
                teamsplit = (tournamentinfo.find('img')['title'])
            except:
                teamsplit = 'error'
            try:
                tournament = (tournamentinfo.find('a')['title'])
            except:
                try:
                    tournament = (tournamentinfo.find('a').text)
                except:
                    tournament = 'error'
            try:
                tournamenturl = (tournamentinfo.find('a')['href'])
            except:
                tournamenturl = 'error'
            try:
                listprize = row.findAll('td', {'class' : 'detail_list_prize'})
            except:
                continue
            try:
                prize = (listprize[1].text)
            except:
                prize = 'error'
            try:
                gamecell  = row.find('td', {'class' : 'detail_list_game'})
                game = (gamecell.find('a').text)
            except:
                game = 'error'
            singlerow.append(playerhandle)
            singlerow.append(playername)
            singlerow.append(playercountry)
            singlerow.append(dob)
            singlerow.append(ptournnumber)
            singlerow.append(tournament_date)
            singlerow.append(tournament_placement)
            singlerow.append(tournament)
            singlerow.append(tournamenturl)
            singlerow.append(teamsplit)
            singlerow.append(prize)
            singlerow.append(game)
            tablerow.append(singlerow)
            singlerow = []
  
    except:
        counter += 1
        pass
    counter +=1
    print('{} of {} complete!').format(counter,len(playerlist))
    sleepvalue = random.uniform(1.5, 3.0)
    sleep(sleepvalue)    
with open('smite_results.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(tablerow)
print('File write success') 
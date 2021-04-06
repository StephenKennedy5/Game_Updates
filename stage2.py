from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from datetime import datetime
from pytz import timezone

def start_yet():
    file1 = open('time.txt','r')
    text = file1.readlines()
    time = text[1][:-1]
    file1.close()

    standard_time = datetime.strptime(time,'%H:%M')
    western = timezone('US/PACIFIC')
    western_time = western.localize(standard_time).strftime('%H:%M')
    current_time = datetime.now().strftime('%H:%M')
    tip_off_time = western_time
    game_start = current_time > tip_off_time

    return game_start

def game_update():
    PATH = 'C:\Program Files (x86)\chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.nba.com/schedule')
    time.sleep(3)
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/button').click()

    except:
        pass

    try:
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/button').click()

    except:
        pass

    game_day = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[3]/section/div/div[2]/div[1]/div[1]/div[1]/h6').text
    num_games = game_day.split('|')[1]
    num_game = num_games.strip().split(' ')[0]

    live_info = [0,5,6,7,8]
    post_info = [0,1,2,3,4]

    today_games = []

    for i in range(0,int(num_game)):
        temp = '/html/body/div[1]/div[2]/div[3]/section/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[' + str(i+1) + ']'
        game = driver.find_element_by_xpath(temp).text
        game_split = game.split('\n')
        if game_split[0] == 'FINAL':
            game_info = [game_split[i] for i in post_info]
        else:
            game_info = [game_split[i] for i in live_info]
        today_games.append(game_info)

    driver.close()

    return today_games

def todays_games(game_update):
    game_schedule = []
    live_games = []
    post_games = []
    for i in range(len(game_update)):
        if game_update[i][0] == 'FINAL':
            home = game_update[i][3]
            away = game_update[i][1]
            home_score = game_update[i][4]
            away_score = game_update[i][2]
            game = 'Final Score was ' + home + ' ' + home_score + ' to ' + away + ' ' + away_score
            post_games.append(game)
        elif game_update[i][0] == 'FINAL/OT':
            home = game_update[i][3]
            home_score = game_update[i][4]
            away = game_update[i][1]
            away_score = game_update[i][2]
            game = 'Final Score was ' + home + ' ' + home_score + ' to ' + away + ' ' + away_score
            post_games.append(game)
        elif game_update[i][0].split(' ')[0] == 'LIVE':
            quarter = game_update[i][0]
            away = game_update[i][1]
            away_score = game_update[i][2]
            home = game_update[i][3]
            home_score = game_update[i][4]
            game = 'The game is currently in the ' + quarter[5:] + ' with ' + home + ' ' + home_score + ' to ' + away + ' ' + away_score
            live_games.append(game)
        else:
            home = game_update[i][2]
            away = game_update[i][1]
            start = game_update[i][0]
            game = 'Game starts at ' + start + ' with ' + home +' home and ' + away + ' away'
            game_schedule.append(game)
    return game_schedule,live_games,post_games

game_start = start_yet()
if game_start == True:
    today_games = game_update()
    game_schedule,live_games,post_games = todays_games(today_games)
else:
    print('Game has not begun yet')

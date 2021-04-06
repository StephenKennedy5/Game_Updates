from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from datetime import datetime
from pytz import timezone

'''Run at 10am to get start time of favorite team game for the night
let person know if there team is not playing '''

def start_time():
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
            game_info = [game_split[z] for z in post_info]
        elif game_split[0] == 'FINAL/OT':
            pass
        elif game_split[0] == 'FINAL/OT2':
            pass
        else:
            game_info = [game_split[z] for z in live_info]
        today_games.append(game_info)

    driver.close()

    # favorite_team = input('Who is your favorite team: ').title()
    favorite_team = 'Nets'

    for games in today_games:
        for game in games:
            if favorite_team in game:
                tip_off = games[0]
                favorite_team_game = games

    split_time = tip_off.split(' ')
    split_time.remove('ET')

    new_time = ' '.join(split_time)
    new_time_standard = datetime.strptime(new_time, '%I:%M %p')
    eastern = timezone('US/Eastern')
    east_time = eastern.localize(new_time_standard)
    pacific = timezone('US/PACIFIC')
    western_time = east_time.astimezone(pacific)
    tip_time = western_time.strftime('%H:%M')

    return today_games,favorite_team, tip_time, favorite_team_game

def time_file(today_games,favorite_team, tip_time, favorite_team_game):
     file1 = open('time.txt','w')
     file1.write(favorite_team + '\n')
     file1.write(tip_time + '\n')
     file1.close()


today_games, favorite_team, tip_time, favorite_team_game = start_time()
time_file(today_games,favorite_team, tip_time, favorite_team_game)

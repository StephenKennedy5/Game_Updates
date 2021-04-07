from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from datetime import datetime
from pytz import timezone
from plyer import notification

'''Run at 10am to get start time of favorite team game for the night
let person know if there team is not playing '''

def start_time():
    PATH = 'C:\Program Files (x86)\chromedriver' #directory of chromedriver for selenium
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(PATH,options=option)
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
        # elif game_split[0] == 'LIVE HALF':
        #     for p in range(len(game_split)):
        #         print(p)
        #         print(game_split[p])
        else:
            game_info = [game_split[z] for z in live_info]
            print(game_info)
        today_games.append(game_info)
        print(i)

    driver.close()

    # favorite_team = input('Who is your favorite team: ').title()
    favorite_team = 'Nets' #hard code for favorite team
    play_tonight = False

    for games in today_games:
        for game in games:
            if favorite_team in game:
                tip_off = games[0]
                favorite_team_game = games
                play_tonight = True

    if play_tonight == True:
        split_time = tip_off.split(' ')
        split_time.remove('ET')
        new_time = ' '.join(split_time)
        new_time_standard = datetime.strptime(new_time, '%I:%M %p')
        eastern = timezone('US/Eastern')
        east_time = eastern.localize(new_time_standard)
        pacific = timezone('US/PACIFIC')
        western_time = east_time.astimezone(pacific)
        tip_time = western_time.strftime('%H:%M')
        tip_time_pm = western_time.strftime('%I:%M %p')
    else:
        tip_time = None
        favorite_team_game = None

    return today_games,favorite_team, tip_time, favorite_team_game, play_tonight,tip_time_pm

def time_file(favorite_team, tip_time, play_tonight):
    if play_tonight == True:
        file1 = open('C:\\Users\\steph\\notification\\time.txt','w') #directory of txt file for output to be read by stage2
        file1.write(favorite_team + '\n')
        file1.write(tip_time + '\n')
        file1.close()
    else:
        file1 = open('C:\\Users\\steph\\notification\\time.txt', 'w') #directory of txt file for output to be read by stage2
        file1.write('Your ' + favorite_team + ' has the night off.')
        file1.close()


today_games, favorite_team, tip_time, favorite_team_game, play_tonight, tip_time_pm = start_time()
time_file(favorite_team, tip_time, play_tonight)

if bool(favorite_team_game) == True:
    notification.notify(
        title='Game Day!',
        message='The ' + favorite_team + ' plays at ' + tip_time_pm + ' tonight.',
        app_icon='C:\\Users\\steph\\notification\\basketball.ico',  #directory of basketball notification
        timeout=10,  # seconds
    )
else:
    notification.notify(
        title='Day Off',
        message= 'The ' + favorite_team + ' has the night off.',
        app_icon='C:\\Users\\steph\\notification\\basketball.ico',  #directory of basketball notification
        timeout=10,  # seconds
    )

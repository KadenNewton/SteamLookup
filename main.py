import requests, time, os
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
import os.path
from os import path, system
import pyshorteners, datetime
import concurrent.futures

system("title " + "Steam Web Scraper")

init(convert=True)

api_key = ''

s = pyshorteners.Shortener()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    print(Fore.CYAN + r'''
  _________ __                            _________                                        
 /   _____//  |_  ____ _____    _____    /   _____/ ________________  ______   ___________ 
 \_____  \\   __\/ __ \\__  \  /     \   \_____  \_/ ___\_  __ \__  \ \____ \_/ __ \_  __ \
 /        \|  | \  ___/ / __ \|  Y Y  \  /        \  \___|  | \// __ \|  |_> >  ___/|  | \/
/_______  /|__|  \___  >____  /__|_|  / /_______  /\___  >__|  (____  /   __/ \___  >__|   
        \/           \/     \/      \/          \/     \/           \/|__|        \/       
''')

def get_user_info(steamuser):
    steam_id = steamuser
    if steam_id.isalpha():
        steam_user_response = requests.get(f'https://www.steamidfinder.com/lookup/{steam_id}')
        soup = BeautifulSoup(steam_user_response.content, 'html.parser')

        id_text = (soup.find("meta", {"name":"description"})['content'])
        numbers = []
        for character in id_text.split():
            if character.isdigit():
                numbers.append(character)
        
        steam_id = ''.join(numbers)

    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'
    response = requests.get(url)
    user_info = response.json()
    return user_info

def get_friend_info(steamuser):
    steam_id = steamuser
    if steam_id.isalpha():
        steam_user_response = requests.get(f'https://www.steamidfinder.com/lookup/{steam_id}')
        soup = BeautifulSoup(steam_user_response.content, 'html.parser')

        id_text = (soup.find("meta", {"name":"description"})['content'])
        numbers = []
        for character in id_text.split():
            if character.isdigit():
                numbers.append(character)
        
        steam_id = ''.join(numbers)

    url = f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend'
    response = requests.get(url)
    user_friend_info = response.json()

    return user_friend_info

def get_steam_games_info(steamuser):
    steam_id = steamuser
    if steam_id.isalpha():
        steam_user_response = requests.get(f'https://www.steamidfinder.com/lookup/{steam_id}')
        soup = BeautifulSoup(steam_user_response.content, 'html.parser')

        id_text = (soup.find("meta", {"name":"description"})['content'])
        numbers = []
        for character in id_text.split():
            if character.isdigit():
                numbers.append(character)
        
        steam_id = ''.join(numbers)

    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
    response = requests.get(url)
    user_game_info = response.json()

    return user_game_info

def get_cost(steamapp):
    steam_id = steamapp
    url = f'https://store.steampowered.com/app/{steam_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        id_text = (soup.find("meta", {"itemprop":"price"})['content'])
    except TypeError:
        id_text = '0'
    return float(id_text)


def verify_api_key(api_key):
    result = requests.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids=76561199146544383')
    soup = BeautifulSoup(result.content, 'html.parser')
    title = soup.find('title')
    try:
        if title.text == 'Forbidden':
            print(Fore.RED + 'Your Api key is not valid\nYou must change it by going to https://steamcommunity.com/dev/apikey\nFor Domain I would recommend just using localhost:8080\n')
            print('Enter your new Api Key here: ', end='')
            new_api_key = input()
            f = open('api-key.txt', 'w+')
            f.write(new_api_key)
            print(Fore.CYAN + '\nPress Enter to exit the program and restart.')
            input()
            exit()
        else:
            print(Fore.GREEN + 'Your Api Key is Verified')
    except AttributeError:
        print(Fore.GREEN + 'Your Api Key is Verified')




if path.exists('api-key.txt') and api_key == '':
    f = open("api-key.txt","r")
    contents = f.read()
    if contents == '':
        print(Fore.CYAN + 'Enter your steam api key: ', end='')
        api_key = input()
        f.close()
        f = open("api-key.txt", "w+")
        f.write(api_key)
        f.close()
    else:
        api_key = contents
    f.close()

elif api_key == '':
    f = open("api-key.txt", "w+")
    print(Fore.CYAN + 'Enter your steam api key: ', end='')
    steam_api_input = input()
    f.write(steam_api_input)
    f.close()


print(Fore.CYAN + 'Verifying Api Key...')
time.sleep(0.5)
verify_api_key(api_key)
time.sleep(0.5)
clear_console()

print_logo()
print('[+]' + Fore.WHITE + ' Created by Kaden#4313\n')
print(Fore.CYAN + '[1]' + Fore.WHITE + ' Look up a Steam Users Details\n')

user_input = input(Fore.CYAN + 'Choice: ' + Fore.WHITE)

show_amount_spent = False

if user_input == '1':
    print(Fore.CYAN + 'Show amount spent on games? (y/n) '+ Fore.WHITE, end='')
    enable_amount_spent = input()
    if enable_amount_spent == 'y':
        show_amount_spent = True
    else:
        show_amount_spent = False
    
    print(Fore.CYAN + 'Enter a steam user/id: ' + Fore.WHITE, end='')
    user_input_id = input()
    user_info = get_user_info(user_input_id)
    user_friend_info = get_friend_info(user_input_id)
    user_game_info = get_steam_games_info(user_input_id)
    clear_console()
    print_logo()

    UserName = user_info['response']['players'][0]['personaname']
    profilePic = user_info['response']['players'][0]['avatarfull']
    status = user_info['response']['players'][0]['personastate']
    time_created = user_info['response']['players'][0]['timecreated']
    profile_url = user_info['response']['players'][0]['profileurl']
    friend_amount = 0
    for i in user_friend_info['friendslist']['friends']:
        friend_amount += 1
    game_amount = user_game_info['response']['game_count']
    total_playtime = 0
    total_money_spent = 0

    
    for i in range(len(user_game_info['response']['games'])):
        clear_console()
        total_playtime += user_game_info['response']['games'][i]['playtime_forever']
        print(f'Getting data of games ({i}/{game_amount})')
        if show_amount_spent == True:
            total_playtime += user_game_info['response']['games'][i]['playtime_forever']
            game_id = user_game_info['response']['games'][i]['appid']

            game_price = get_cost(game_id)

            total_money_spent += float(game_price)
    

    
    clear_console()
    print_logo()


    if status == 0:
        status = 'Offline'
    elif status == 1:
        status = 'Online'
    elif status == 2:
        status = 'Busy'
    elif status == 3:
        status = 'Away'
    elif status == 4:
        status = 'Snooze'
    elif status == 5:
        status = 'Looking to trade'
    elif status == 6:
        status = 'Looking to play'
    else:
        status = 'Private'

    print(Fore.CYAN +'User: ' + Fore.WHITE + str(UserName))
    print(Fore.CYAN + 'Profile Pic: ' + Fore.WHITE + str(s.tinyurl.short(profilePic)))
    print(Fore.CYAN + 'Status: ' + Fore.WHITE + str(status))
    print(Fore.CYAN + 'Date Created: ' + Fore.WHITE + str(datetime.datetime.fromtimestamp(time_created).strftime('%Y-%m-%d %H:%M:%S')))
    print(Fore.CYAN + 'Profile Url: ' + Fore.WHITE + str(profile_url))
    print(Fore.CYAN + 'Friends: ' + Fore.WHITE + str(friend_amount))
    print(Fore.CYAN + 'Games Owned: ' + Fore.WHITE + str(f'{game_amount:,}'))
    print(Fore.CYAN + 'Total Playtime: ' + Fore.WHITE + str(f'{int(total_playtime / 60):,} hours'))
    if show_amount_spent == True:
        print(Fore.CYAN + 'Total Spent on Games: ' + Fore.WHITE + str(f'${int(total_money_spent):,}'))
    input()
    


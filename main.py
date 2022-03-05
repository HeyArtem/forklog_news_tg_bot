from asyncore import read
from urllib import request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import os
import json


'''
Сначала я хотел парсить Известия, но там мало новостей про крипту
Первая функция парсит сайт, записывает его в json
вторая при запуске сверяет со старым json есть ли новые карточки и записывает его в новый json

Я хочу это запустить на сервере и настроить регулфрную отправку себе в телегу
'''


def get_data():
    ua = UserAgent()
    url = 'https://forklog.com/'
    
    headers = {
        'user-agent': 'ua.random',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'        
    }
    
    response = requests.get(url=url, headers=headers)
    
    if not os.path.exists('forklog_news'):
        os.mkdir('forklog_news')
        
    with open('forklog_news/index.html', 'w') as file:
        file.write(response.text)
        
    with open('forklog_news/index.html') as file:
        src = file.read()
        
    soup = BeautifulSoup(markup=src, features='lxml')
    
    # в этот словарь буду записывать карточки
    all_cards_dict = {}
    
    # общий блок
    all_cards = soup.find_all('div', class_='post_item')
    
    for card in all_cards:
        
        # title
        item_card = card.find('div', class_="text_blk").text.strip().split()
        item_title = ' '.join(item_card)
        
        # url
        item_url = card.find('a').get('href')
        
        all_cards_dict[item_title] = item_url
        # print(f"{item_title}: {item_url}\n{20*'*-'}")
        
    with open('forklog_news/all_cards.json', 'w') as file:
        json.dump(all_cards_dict, file, indent=4, ensure_ascii=False)
        
        
'''
Функция парсит и сравнивает новую информацию
со строй. Создает новый словарь и перезаписывает старый
'''
def get_fresh_data(path='forklog_news/all_cards.json'):
    
    # сохраняю в переменную результаты старого парсинга
    with open(file=path) as file:
        src = json.load(file)
    
    # подмена юзерагента
    ua = UserAgent
    url = 'https://forklog.com/'
    
    headers = {
        'user-agent': 'ua.random',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'        
    }
    
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(markup=response.text, features='lxml')
    
    # общий блок с карточками
    all_cards = soup.find_all('div', class_='post_item')
    
    all_fresh_cards_dict = {}

    for card in all_cards:
    
        # title
        item_card = card.find('div', class_="text_blk").text.strip().split()
        item_title = ' '.join(item_card)
        
        # если новый title есть в старом словаре, шарюсь дальше
        if item_title in src:
            continue
        
        # если есть новый title, нахожу url 
        else:            
            # url
            item_url = card.find('a').get('href')
        
            # новый title & url заношу в новый словарь
            all_fresh_cards_dict[item_title] = item_url # Макс где здесь отступ????????????????????
            
            # также в старый словарь заношу новые данные (старые + дозаписал новые)
            src[item_title] = item_url
            
        # новый словарь записал в новый json
        with open(file='forklog_news/all_fresh_cards.json', mode='w') as file:
            json.dump(all_fresh_cards_dict, file, indent=4, ensure_ascii=False)
            
        # старый словарь (+ с новыми данными) перезаписал в старый json
        with open(file='forklog_news/all_cards.json', mode='w') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)
            
        return all_fresh_cards_dict


# def main():
#     # get_data()
#     get_fresh_data()


# if __name__ == '__main__':
#     main()

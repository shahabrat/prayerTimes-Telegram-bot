'''
import requests
from bs4 import BeautifulSoup
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
URL='https://shosh.uz/namoz-vaqtlari-toshkent-shahri/'
# import json
# city='Tashkent'
# url=f'http://api.pray.zone/v2/times/today.json?city={city}&school=2'
# response=requests.get(url)
# data=response.json()
# print(data)
def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    from datetime import date
    today=date.today()
    t_day = int(today.strftime("%d"))+1
    if t_day%2==0:
        par='even'
    else:
        par='odd'
    items = soup.find_all('tr',class_=f'row-{t_day} {par}')
    news = []
    for item in items:
            news.append(
                {
                    'day': item.find('td', class_='column-1').get_text(strip=True),
                    'weekday': item.find('td', class_='column-2').get_text(strip=True),
                    'tong': item.find('td', class_='column-3').get_text(strip=True),
                    'quyosh': item.find('td', class_='column-4').get_text(strip=True),
                    'peshin': item.find('td', class_='column-5').get_text(strip=True),
                    'asr': item.find('td', class_='column-6').get_text(strip=True),
                    'shom': item.find('td', class_='column-7').get_text(strip=True),
                    'xufton': item.find('td', class_='column-8').get_text(strip=True)
                }
            )
    return news

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        html = get_html(URL)
        news.extend(get_content(html.text))
        req=input('Qaysi namozning vaqtini ko\'rishni xohlaysiz?')
        print(news[0][req])
    else:
        print('Error')
'''
import logging
from aiogram import Bot, Dispatcher, executor, types
import wikipedia
API_TOKEN = '#'

wikipedia.set_lang('uz')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
button_tong=KeyboardButton('tong')
button_quyosh = KeyboardButton('quyosh')
button_peshin=KeyboardButton('peshin')
button_asr=KeyboardButton('asr')
button_shom=KeyboardButton('shom')
button_xufton=KeyboardButton('xufton')
greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_tong,button_quyosh,button_peshin,button_asr,button_shom,button_xufton)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
     await message.reply("Salom!Namoz vaqtlari botiga xush kelibsiz!\nQaysi namoz vaqtini bilishn istaysiz?",reply_markup=greet_kb)



@dp.message_handler()
async def summary(message: types.Message):
    import requests
    from bs4 import BeautifulSoup
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    URL = 'https://shosh.uz/namoz-vaqtlari-toshkent-shahri/'

    # import json
    # city='Tashkent'
    # url=f'http://api.pray.zone/v2/times/today.json?city={city}&school=2'
    # response=requests.get(url)
    # data=response.json()
    # print(data)
    def get_html(url):
        r = requests.get(url, headers=HEADERS)
        return r

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        from datetime import date
        today = date.today()
        t_day = int(today.strftime("%d")) + 1
        if t_day % 2 == 0:
            par = 'even'
        else:
            par = 'odd'
        items = soup.find_all('tr', class_=f'row-{t_day} {par}')
        news = []
        for item in items:
            news.append(
                {
                    'day': item.find('td', class_='column-1').get_text(strip=True),
                    'weekday': item.find('td', class_='column-2').get_text(strip=True),
                    'tong': item.find('td', class_='column-3').get_text(strip=True),
                    'quyosh': item.find('td', class_='column-4').get_text(strip=True),
                    'peshin': item.find('td', class_='column-5').get_text(strip=True),
                    'asr': item.find('td', class_='column-6').get_text(strip=True),
                    'shom': item.find('td', class_='column-7').get_text(strip=True),
                    'xufton': item.find('td', class_='column-8').get_text(strip=True)
                }
            )
        return news

    def parser():
        html = get_html(URL)
        if html.status_code == 200:
            news = []
            html = get_html(URL)
            news.extend(get_content(html.text))
            req = message.text
            global answer
            answer=news[0][req]
        else:
            answer='Error'
    parser()
    await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
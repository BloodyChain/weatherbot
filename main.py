import time
import telebot
from telebot import types
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
parse_text = []
current_index = {}
loading = ['🌑', '🌑🌒', '🌑🌒🌓', '🌑🌒🌓🌔', '🌑🌒🌓🌔🌕',
           '🌑🌒🌓🌔🌕🌖', '🌑🌒🌓🌔🌕🌖🌗', '🌑🌒🌓🌔🌕🌖🌗🌘']


def parse_site(chat_id, message_id):
    parse_text.clear()
    soup = driver_conn("https://yandex.ru/pogoda/ru?lat=59.941452&lon=30.467628")
    try:
        short_widget = soup.find('article', class_='MainPage_appForecast__W17xR')
    except Exception as e:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='😞Ошибка получения данных😞')
        return
    single_widget = short_widget.find_all('a')
    for i in single_widget:
        pred = i.find('p')
        tom1_text = re.sub('; ', '\n\n', pred.text)
        tom_text = re.sub(': ', '\n\n', tom1_text, count=1)
        parse_text.append(tom_text)


def driver_conn(urla):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(urla)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "visuallyHidden"))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def btn_back(callback_data):
    btnback = types.InlineKeyboardButton(text='◀ Назад', callback_data=callback_data)
    return btnback


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton(text='Начать!', callback_data='vars')
    markup.add(btn_start)
    bot.send_message(message.chat.id, "Привет! 😃\nЯ помогу тебе узнать погоду на улице! ⛅",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'vars')
def btn_strt(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='🌡 Узнать погоду', callback_data='wthr')
    btn2 = types.InlineKeyboardButton(text='🌐 Перейти на сайт', callback_data='url')
    markup.add(btn1, btn2)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='🌷 Выберите интересующее вас действие 🌷', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'url')
def url(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    markup = types.InlineKeyboardMarkup()
    btn_weather = types.InlineKeyboardButton(text='Перейти на Яндекс.Погоду', url='https://yandex.ru/pogoda/ru')
    markup.add(btn_weather, btn_back('vars'))
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text="Посмотри погоду в Яндексе!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'wthr')
def info(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    markup = types.InlineKeyboardMarkup()
    btn_today = types.InlineKeyboardButton(text='24 часа', callback_data='today')
    btn_tomorrow = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    btn_tomtomorrow = types.InlineKeyboardButton(text='10 дней', callback_data='10_days')
    markup.add(btn_today, btn_tomorrow, btn_tomtomorrow, btn_back('vars'))
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text="🌞 Выберите дату, на которую вы хотите узнать погоду!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'today')
def today_weather(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id

    for moon in loading:
        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text=f"⚡Скачиваем данные так быстро, как можем!⚡\n\n{moon}")
            time.sleep(0.5)
        except:
            pass

    markup = types.InlineKeyboardMarkup()
    markup.add(btn_back('wthr'))
    soup = driver_conn("https://yandex.ru/pogoda/ru?lat=59.941452&lon=30.467628")
    try:
        ul_widget = soup.find('ul', class_='AppHourly_list__gXAeN')
        p_widget = ul_widget.find_all('p')
    except Exception as e:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='😞Ошибка получения данных😞')
        return
    today_text = '\n'
    for p in p_widget:
        if 'Ощущается' in p.text:
            normal_string = re.sub(', Ощущается как \\S\\d{1,3}\\S', '', p.text)
            today_text += normal_string + '\n'
    bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                          text='⭐Погода на ближайшие 24 часа⭐\n\n' + today_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'tomorrow')
def tomorrow_weather(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id

    for moon in loading:
        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text=f"🌩Высматриваем тучки вдалеке!🌩\n\n{moon}")
            time.sleep(0.5)
        except:
            pass

    markup = types.InlineKeyboardMarkup()
    markup.add(btn_back('wthr'))

    soup = driver_conn("https://yandex.ru/pogoda/ru?lat=59.941452&lon=30.467628")
    tom1 = datetime.date.today() + datetime.timedelta(days=1)
    tom = tom1.day
    try:
        a_tom = soup.find('a', attrs={'data-id': fr'd_{tom}'})
        div_tom = a_tom.find('p', class_='A11Y_visuallyHidden__y0sw0 visuallyHidden')
    except Exception as e:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='😞Ошибка получения данных😞')
        return
    tom1_text = re.sub('; ', '\n\n', div_tom.text)
    tom_text = re.sub(': ', '\n\n', tom1_text, count=1)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=tom_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == '10_days')
def sever_days(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id

    for moon in loading:
        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text=f"💨Путешествуем во времени, чтобы ответить вам!💨\n\n{moon}")
            time.sleep(0.5)
        except:
            pass

    parse_site(chat_id, message_id)
    current_index[chat_id] = 0
    current_pos = current_index.get(chat_id, 0)
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton(text='◀', callback_data='prev')
    btn_next = types.InlineKeyboardButton(text='▶', callback_data='next')
    markup.add(btn_prev, btn_back('wthr'), btn_next)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=parse_text[current_pos], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['prev', 'next'])
def prev_days(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    new_index = -2
    if chat_id not in current_index:
        current_index[chat_id] = 0
    if call.data == 'prev':
        new_index = ((current_index[chat_id] - 1) + (len(parse_text))) % (len(parse_text))
    elif call.data == 'next':
        new_index = (current_index[chat_id] + 1) % (len(parse_text))
    if new_index == current_index[chat_id]:
        bot.answer_callback_query(call.id)
        return
    current_index[chat_id] = new_index
    current_pos = current_index.get(chat_id, 0)
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton(text='◀', callback_data='prev')
    btn_next = types.InlineKeyboardButton(text='▶', callback_data='next')
    markup.add(btn_prev, btn_back('wthr'), btn_next)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=parse_text[current_pos], reply_markup=markup)



bot.polling(none_stop=True, interval=1)

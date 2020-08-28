
# -*- coding: utf-8 -*-

import os.path
import telebot
import sys
import re
import sqlite3
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

token = '1111'
bot = telebot.TeleBot(token)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "homekredit.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
punct = ('(',',',')','\'',']')
translation_table = dict.fromkeys(map(ord, punct))
fortv = r'TV'
main_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add('Товары','Настройки')
tovar_rus = telebot.types.InlineKeyboardMarkup()
teliki_rus = telebot.types.InlineKeyboardButton(text='ТЕЛЕВИЗОРЫ, АНТЕННЫ, DVD-BLU-RAY ПЛЕЙЕРЫ', callback_data='teliki')
holodilniki_rus = telebot.types.InlineKeyboardButton(text='ХОЛОДИЛЬНИКИ И МОРОЗИЛЬНИКИ', callback_data='colds')
wash_machine_rus = telebot.types.InlineKeyboardButton(text='СТИРАЛНЫЕ МАШИНЫ (АВТОМАТЫ и ПОЛУАВТОМАТЫ)', callback_data='wash')
pilesosi_rus = telebot.types.InlineKeyboardButton(text='ПЫЛЕСОСЫ', callback_data='pilesosi')
condition_rus = telebot.types.InlineKeyboardButton(text='КОНДИЦИОНЕРЫ', callback_data='condition')
gas_rus = telebot.types.InlineKeyboardButton(text='ГАЗОВЫЕ, ЭЛЕКТРИЧЕСКИЕ И КОМБИНИРОВАННЫЕ ПЛИТЫ', callback_data='gas')
let_25_rus = telebot.types.InlineKeyboardButton(text='МИКРОВОЛНОВКИ И ЭЛЕКТРОПЛИТЫ', callback_data='let_25')
vityajki_rus = telebot.types.InlineKeyboardButton(text='ВЫТЯЖКИ И ВОДОНАГРЕВАТЕЛИ', callback_data='vityajki')
noteboks_rus = telebot.types.InlineKeyboardButton(text='НОУТБУКИ, УЛЬТРАБУКИ', callback_data='notes')
comps_rus = telebot.types.InlineKeyboardButton(text='МОНИТОРЫ, ПРИНТЕРЫ, МФУ, МОДЕМЫ, ФЛЕШКИ, …', callback_data='comps')
sounds_rus = telebot.types.InlineKeyboardButton(text='АКУСТИКА (КОЛОНКИ, САБВУФЕРЫ)', callback_data='sounds')
mobi_rus = telebot.types.InlineKeyboardButton(text='МОБИЛЬНЫЕ ТЕЛЕФОНЫ И ПЛАНШЕТЫ', callback_data='mobi')
photo_rus = telebot.types.InlineKeyboardButton(text='ФОТОАППАРАТЫ И КАМЕРЫ (ОБЫЧНЫЕ И ЗЕРКАЛЬНЫЕ)', callback_data='photo')
small_rus = telebot.types.InlineKeyboardButton(text='МЕЛКО-БЫТОВОЙ', callback_data='small')
tovar_rus.add(teliki_rus)
tovar_rus.add(holodilniki_rus)
tovar_rus.add(wash_machine_rus)
tovar_rus.add(pilesosi_rus)
tovar_rus.add(condition_rus)
tovar_rus.add(gas_rus)
tovar_rus.add(let_25_rus)
tovar_rus.add(vityajki_rus)
tovar_rus.add(noteboks_rus)
tovar_rus.add(comps_rus)
tovar_rus.add(sounds_rus)
tovar_rus.add(mobi_rus)
tovar_rus.add(photo_rus)
tovar_rus.add(small_rus)

def remove_punctuation(text):
    return text.translate(translation_table)

@bot.message_handler(commands=['start'])
def start(message):
    cursor = conn.cursor()
    cursor.execute("select id_tg from 'users' where id_tg='"+str(message.from_user.id)+"'")
    l=cursor.fetchall()
    if l.__len__()>0:
        bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=main_markup)
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать! \n Язык по умолчанию Русский 🇷🇺'+
                                          '\n Вы можете поменять язык в найстройках'+
                                          '\n You can chage your language in options'+
                                            '\n po uzbeksi')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users ([id_tg],[lang]) values (" + str(message.from_user.id) + ",'rus')")
        conn.commit()

@bot.message_handler(content_types=['text'])
def factoring(message):
    if message.text==u'stop':
        bot.send_message(message.chat.id, 'Выключаюсь')
        sys.exit(0)
    elif message.text == u'Товары':
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=tovar_rus)
    else:
        bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda c: True)
def factorin(c):
    if re.match(fortv,c.data):
        cursor = conn.cursor()
        cursor.execute("select post from 'tv' where name='"+c.data[3:]+"'")
        post = cursor.fetchall()
        bot.send_message(chat_id=c.message.chat.id, text=post[0][0].encode('utf-8'))
    elif c.data=='teliki':
        cursor = conn.cursor()
        cursor.execute("select name from 'tv'")
        rows = cursor.fetchall()
        nbs = list(rows)
        p = []
        for addition in nbs:
            nb_str = 'TV ' + str(addition)
            p.append(remove_punctuation(nb_str))
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in p])
        bot.send_message(c.message.chat.id, "Телевизоры", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)


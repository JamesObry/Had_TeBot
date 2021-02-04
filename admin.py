import telebot
from telebot import types
import sqlite3 as sq

with sq.connect("vebinar.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS admin (
        telegram_id INTEGER PRIMARY KEY,
        message_text TEXT
    )""")

# keyboards
mainKeyboard = types.InlineKeyboardMarkup()
mainKey = types.InlineKeyboardButton(text='Сделать рассылку', callback_data='sendMessage')
mainKeyboard.add(mainKey)

bot = telebot.TeleBot('1618891760:AAEHOZP36ngovy_f_5fC-Bs1Wi4Apyi9JpA')

@bot.message_handler(commands=['start'])
def startMessage(message):
    with sq.connect("vebinar.db") as con:
        cur = con.cursor()
        # cur.execute(f"insert into admin(telegram_id) values ({message.chat.id})")
        try:
            cur.execute(f"SELECT telegram_id FROM admin WHERE telegram_id = {message.chat.id}")
            id = cur.fetchone()[0]
            if id == admin id:
                bot.send_message(message.chat.id, 'Доступ открыт. ✅', reply_markup=mainKeyboard)
            elif id != admin id:
                bot.send_message(message.chat.id, 'Доступ закрыт. ❌')
        except:
            bot.send_message(message.chat.id, 'У вас нету доступа к этому разделу. ❌')

@bot.callback_query_handler(func=lambda call: True)
def check(call):
    bot.send_message(call.message.chat.id, 'Введите текст для рассылки.')
    bot.register_next_step_handler(call.message, sendMessage)

def sendMessage(message):
    with sq.connect("vebinar.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE admin SET message_text = '{message.text}' WHERE telegram_id = {message.chat.id}")

bot.infinity_polling(True)

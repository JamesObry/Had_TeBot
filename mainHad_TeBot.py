import telebot
import sqlite3 as sq
from telebot import types

bot = telebot.TeleBot('1689882063:AAHfaQZb196hQ9Hh2VqNMhwYSewGJtnTce0')

with sq.connect("vebinar.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS v_users (
        id INTEGER PRIMARY KEY,
        name TEXT
    )""")

# keyboards
mainBoard = types.InlineKeyboardMarkup(row_width=1)
mainYesKey = types.InlineKeyboardButton(text='100% уверен', callback_data='yes')
mainNoKey = types.InlineKeyboardButton(text='пока не решил', callback_data='no')
mainBoard.add(mainYesKey, mainNoKey)

@bot.message_handler(commands=['start'])
def startMessage(message):
    try:
        with sq.connect("vebinar.db") as con:
            cur = con.cursor()
            name = cur.execute(f"SELECT name FROM v_users WHERE id = {message.chat.id}")
            name = cur.fetchone()[0]
            bot.send_message(message.chat.id, f'Привет {name}!\nС возвращением. Напоминаю что совсем скоро стартует новый вебинар. На сей раз это не просто БЕСПЛАТНЫЙ вебинар, о нет... Это целый мини-курс, где вы получите очень много полезной информации которую вы будете сразу внедрять в свою жизнь.😎')
            bot.send_message(message.chat.id, 'А теперь последний и одновременно самый важный вопрос👇\n\nОтветьте( только честно ) - вы действительно думаете что этот вебинар даст пользу?\n\nИли нет?:)', reply_markup=mainBoard)
    except:
        bot.send_message(message.chat.id,'Привет!\nНапиши пожалуйста как тебя зовут, чтобы я знала как к тебе обращаться)')
        bot.register_next_step_handler(message, saveName)
def saveName(message):
    try:
        with sq.connect("vebinar.db") as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO v_users (id, name) VALUES (?, ?)", (message.chat.id, message.text))
    except:
        pass
    bot.send_message(message.chat.id, 'А теперь последний и одновременно самый важный вопрос👇\n\nОтветьте( только честно ) - вы действительно думаете что этот вебинар даст пользу?\n\nИли нет?:)', reply_markup = mainBoard)

@bot.callback_query_handler(func=lambda call:True)
def startMessageCheck(call):
    if call.data == 'no':
        bot.send_message(call.message.chat.id, 'Есть только один способ узнать)\n\nКак я уже и сказала - начинаем 00 "месяц" в 00:00 мск.\n\nНа сей раз это не просто БЕСПЛАТНЫЙ вебинар, о нет... Это челый мини-курс, где вы получите очень много полезной информации которую вы будете сразу внедрять в свою жизнь.😎')
    elif call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Отлично!🚀\n\nКак я уже сказала - начинаем 00 "месяц" в 00:00 мск.\n\nНа сей раз это не просто БЕСПЛАТНЫЙ вебинар, о нет... Это целый мини-курс, где вы получите очень много полезной информации которую вы будете сразу внедрять в свою жизнь.😎')







bot.infinity_polling(True)
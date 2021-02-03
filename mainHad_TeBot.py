import telebot
import time
import sqlite3 as sq
from telebot import types

with sq.connect("vebinar.db") as con:
    cur = con.cursor()
    cur.execute("""create table if not exists vebinar_users (
        telegram_id integer primary key,
        name text,
        f_que text
    )""")
    cur.execute("""create table if not exists admin (
        telegram_id integer primary key,
        message_text text,
        previous_text text
    )""")

bot = telebot.TeleBot('1689882063:AAHfaQZb196hQ9Hh2VqNMhwYSewGJtnTce0')

# keyboards
main_question = types.InlineKeyboardMarkup(row_width=1)
mainYes = types.InlineKeyboardButton(text='100% уверен', callback_data='yes')
mainNo = types.InlineKeyboardButton(text='Пока не решил', callback_data='no')
main_question.add(mainYes,mainNo)

@bot.message_handler(commands=['start'])
def startMessage(message):
    with sq.connect("vebinar.db") as con:
        cur = con.cursor()
        try:
            user_name = cur.execute(f"select name from vebinar_users where telegram_id = {message.chat.id}")
            user_name = cur.fetchone()[0]
            bot.send_message(message.chat.id, f'С возвращением {user_name}')
            f_q = cur.execute(f'select f_que from vebinar_users where telegram_id = {message.chat.id}')
            f_q = cur.fetchone()[0]
            if f_q == 'нет':
                bot.send_message(message.chat.id,'Ответь пожалуйста на последний, но одновременно самый важный вопрос👇\n\nТы действительно думаешь что этот вебинар дайст пользу?\n\nИли нет?:)',reply_markup=main_question)
            elif f_q == 'да':
                bot.send_message(message.chat.id,'Как я уже сказала начинаем 1 января в 14:60 мск.\n\nНа сей раз это не просто БЕСПЛАТНЫЙ вебинар, о нет... Это целый мини-курс, где вы получите очень много полезной информации которую будете сразу внедрять в свою жизнь😎')
                bot.send_message(message.chat.id, 'Ожидай уведомлений про вебинар, я буду тебя там ждать!')
        except:
            bot.send_message(message.chat.id, 'Напиши пожалуйста свое имя, чтобы я знала как к тебе обращаться')
            bot.register_next_step_handler(message, rename)
def rename(message):
    with sq.connect("vebinar.db") as con:
        cur = con.cursor()
        name = message.text
        cur.execute(f"insert into vebinar_users(name, telegram_id, f_que) values (?, ?, ?)", (message.text, message.chat.id, 'нет'))
        bot.send_message(message.chat.id, f'Привет {name}')
        bot.send_message(message.chat.id, 'Ответь пожалуйста на последний, но одновременно самый важный вопрос👇\n\nТы действительно думаешь что этот вебинар дайст пользу?\n\nИли нет?:)', reply_markup=main_question)
@bot.callback_query_handler(func=lambda call:True)
def f_queCheck(call):
    if call.data == 'yes':
        with sq.connect("vebinar.db") as con:
            cur = con.cursor()
            cur.execute(f"update vebinar_users set f_que = 'да' where telegram_id = {call.message.chat.id}")
            bot.send_message(call.message.chat.id, 'Отлично!🚀\n\nКак я уже сказала начинаем 1 января в 14:60 мск.\n\nНа сей раз это не просто БЕСПЛАТНЫЙ вебинар, о нет... Это целый мини-курс, где вы получите очень много полезной информации которую будете сразу внедрять в свою жизнь😎')
    elif call.data == 'no':
        with sq.connect("vebinar.db") as con:
            cur = con.cursor()
            cur.execute(f"update vebinar_users set f_que = 'нет' where telegram_id = {call.message.chat.id}")
            bot.send_message(call.message.chat.id, 'Есть только один способ узнать)\n\nПодумать и решить точно ')

def sendMessage(message):
    time.sleep(10)
    with sq.connect("vebinar.db") as con:
        cur = con.cursor()
        cur.execute("select message_text from admin where telegram_id = 'myid'")
# TO DO
# ADMIN BOT
# ADMIN DB
# WITH BOOL ADN DB
bot.infinity_polling(True)
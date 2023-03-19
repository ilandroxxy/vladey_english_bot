import telebot
from telebot import types
import sqlite3
import random
import time

with open("token.txt") as f1, open("creators.txt") as f2:
    TOKEN = f1.read().strip()
    CREATORS = [int(i) for i in f2.read().strip().split()]

bot = telebot.TeleBot(TOKEN)
# 👉 🙏 👆 👇 😅 👋 🙌 ☺️ ❗️‼️ ✌️ 👌 ✊ 👨‍💻
# 🤖 😉  ☝️ ❤️ 💪 ✍️ 🎯  ⛔ ️✅ 📊📈🧮   🗳️


# region Функция для обработки запросов с inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def step(call):

    if call.data == 'call_key_1':
        pass

    elif call.data == 'call_key_2':
        pass
# endregion Функция для обработки запросов с inline кнопок

# region Команда: /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Записаться 🗳️", url="https://planerka.app/meet/vladislav.galkov"))

    sql = sqlite3.connect('sqlite3.db')
    cursor = sql.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                                                      id INTEGER,
                                                      username TEXT,
                                                      firstname TEXT,
                                                      lastname TEXT
                                                      )""")
    sql.commit()

    cursor.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
    users_records = cursor.fetchone()

    if users_records is None:
        cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?);", (message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name))
        sql.commit()

        bot.send_message(message.chat.id, f"⚡️Занятия по Смитам⚡️", reply_markup=markup, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f"⚡️Занятия по Смитам⚡️", reply_markup=markup, parse_mode='Markdown')
# endregion Команда: /start


# region Команда: /getmyid
@bot.message_handler(commands=['getmyid'])
def getmyid(message):
    user = str(message.chat.id)
    send_message = "👾 Если интересно, то вот *твой user ID: *" + user
    bot.send_message(message.chat.id, send_message, parse_mode="Markdown")
# endregion Команда: /getmyid


# region Команда: /Отправить файлы db 💾
@bot.message_handler(commands=['db'])
def db(message):
    if message.chat.id in CREATORS:
        db = open("sqlite3.db", 'rb')
        bot.send_document(message.chat.id, db)
    else:
        bot.send_message(message.chat.id, "Извините, у вас нет прав доступа 👨‍💻")
# endregion Команда: /Отправить файлы db 💾


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()

    if get_message_bot == "привет":
        bot.send_message(message.chat.id, f'Hi! How are you?', parse_mode='Markdown')

    elif get_message_bot == "как дела?":
        bot.send_message(message.chat.id, f'Hi! How are you?', parse_mode='Markdown')

    # region Если бот не может ответить
    else:
        send_message = ['Когда–нибудь мы захватим мировое правительство..🤖👾',
                        'Хм, интересно, но не совсем понятно 🤔',
                        'Это что-то новое, я такого не встречал 🤔',
                        'Я не уверен, что правильно понимаю вопрос 🤔',
                        'Надо бы уточнить детали, чтобы было яснее 🧐',
                        'Кажется, здесь есть некоторое недопонимание 🤔',
                        'Не очень ясно, что ты имеешь в виду 🤔',
                        'Мне кажется, что мы говорим о разных вещах 🤔',
                        'Ну это же просто!... Нет, это я шучу, я не понимаю 🤣',
                        'Это какой-то совсем новый уровень сложности для меня 🙃',
                        'Может, я где-то потерял нить разговора? 🤔',
                        'Пока что не могу сказать, что понимаю 🤔',
                        'Я не уверен, что это входит в мой функционал 🤖',
                        'Видимо, это надо спросить у другого бота 🤖',
                        'Извини, я не очень хорошо в этом разбираюсь 🙁',
                        'Кажется, это не моя стихия, извини 😕',
                        'Я не уверен, что смогу помочь с этим 🤔',
                        'Может быть, попробуем переформулировать вопрос? 🤔',
                        'Я стараюсь, но не всегда могу понять, о чем речь 🤷‍',
                        'Это явно выходит за рамки моих возможностей 🤖',
                        'Надо бы разобраться в этом более детально 🤔',
                        'Не совсем ясно, что здесь происходит 🤔',
                        'У меня нет ответа на этот вопрос, извини 🙁',
                        'Может быть, это не мой круг компетенций 🤖',
                        'Ну это как-то совсем неочевидно 🤔',
                        'Мне нужно больше информации, чтобы сказать что-то определенное 🧐',
                        'Кажется, здесь что-то не так 🤔',
                        'Возможно, мы говорим на разных языках 🤷‍',
                        'Честно говоря, я понимаю только каждое третье слово 🤔',
                        'Извини, я не могу тебе помочь в этом 🙁',
                        'Мне кажется, здесь нужно пройти обучение, чтобы разобраться']
        bot.send_message(message.chat.id, random.choice(send_message))
    # endregion Если бот не может ответить

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)

import telebot
from telebot import types
import time
from parse_giftery import parse_giftery

TOKEN = '5250162868:AAFh073tGGZOBZfSAAhfXhspfRHsgsLeD8k'

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    bot.reply_to(message,f"Здраствуйте, {user_first_name} {user_last_name}! С помощью этого Бота Вы можете найти описание подарочных карт,"
                       " продающихся на сайте Giftery")
    time.sleep(3)
    bot.send_message(message.chat.id,"Для начала поиска выберете команду /search и выберете раздел, в котором надо найти карту."
                                     " После обработки запроса Вы получите файл в формате .txt, "
                                     "содержащий следующую информацию: Наименование карты, Описание карты, Возможный номинал, ссылка на"
                                     "сайт, где можно приобрести карту")

@bot.message_handler(commands=['search'])
def search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Развлечения")
    btn2 = types.KeyboardButton("Игры")
    btn3 = types.KeyboardButton("Товары для дома")
    btn4 = types.KeyboardButton("Украшения")
    btn5 = types.KeyboardButton("Путешествия")
    btn6 = types.KeyboardButton("Образование")
    btn7 = types.KeyboardButton("Продукты")
    btn8 = types.KeyboardButton("Книги")
    btn9 = types.KeyboardButton("Спорт")
    markup.add(btn1, btn2, btn3, btn4, btn5,btn6,btn7,btn8,btn9)
    bot.send_message(message.chat.id,"Для выбора типа карты нажмите на кнопку ниже", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
        bot.reply_to(message,f"Данный Телеграм бот помогает найти информацию о подарочных картах,"
                             f" продающихся на сайте Giftery. Для начала поиска необходимо вызваь команду /search "
                             f"и затем из появившегося меню выбрать раздел подарочных карт, о которых Вы хотели бы получить "
                             f"информацию. Либо можно отправить сообщение боту с одним из названий раздела из списка:"
                             f"Развлечения, Игры, Товары для дома, Украшения, Путешествия, Образование, Продукты, Книги, Спорт."
                             f"Результат придет в виде текстового файла, в котором будет описание доступных на момент запроса "
                             f"подарочных карт")


@bot.message_handler(content_types=['text'])
def searchtext(message):
    visitor_message = message.text
    buttons=["Развлечения","Игры","Товары для дома","Украшения","Путешествия","Образование","Продукты","Книги","Спорт"]
    if visitor_message in buttons:
        card_types = {"Развлечения": "hobby", "Товары для дома": "homegoods", "Украшения": "jewellery", "Красота": "beauty", "Игры": "games", '6': "services",
                  "7": "spa", "Книги": "books", "Спорт": "sport", "10": "cafe", "Путешествия": "travel", "Продукты": "food", "Образование": "education",
                  "14": "kids"
                  }
        section = card_types[visitor_message]
        bot.send_message(message.chat.id, "Подождите Ваш запрос обрабатывается....")
        parse_giftery(section)
        file = open("giftcards.txt", "rb")
        bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "Я Вас не понял. Нажмите кнопку интересующего Вас раздела еще раз")


bot.polling()

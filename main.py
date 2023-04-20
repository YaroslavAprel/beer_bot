import telebot
import pymysql
from telebot import types
from db import DataBase
import datetime

bot = telebot.TeleBot("2107269188:AAH-WJMXjjs_YECMO-u25Tgymi8E_5sZNwg")
db = DataBase('localhost', 'root', 'Morgretar2023', 'beer')
info = {}
admin = ['810885387']
data = datetime.datetime.now()
order = []
quant = []
addresses = []
address = ""
comment = ""

@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = message.from_user.id
    if user_id == int(admin[0]):
        bot.send_message(message.chat.id, "Вы верховный администратор бота")
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_drinks = types.KeyboardButton("Заказ")
    button_util = types.KeyboardButton("Списание")
    button_repair = types.KeyboardButton("Ремонт")
    button_help = types.KeyboardButton("Помощь")
    buttons.add(button_drinks, button_util, button_repair, button_help)
    bot.send_message(message.chat.id, "Добро пожаловать! Проследуй в меню, изучи, сделай заказ. Если что-то пойдет не так или потребуется помощь то ты всегда можешь написать Помощь", reply_markup=buttons)


@bot.message_handler(content_types=['text'])
def get_name_drinks(message):
    global order
    global info
    global quant
    global addresses
    global comment
    #user_id = message.from_user.id
    if message.text == "Заказ":

        buttons = types.InlineKeyboardMarkup()
        for i in db.get_type_drink():
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        bot.send_message(message.chat.id, "Выбери категорию напитков", reply_markup=buttons)
    elif message.text == "Заказы":
        for i in db.get_orders():
            bot.send_message(message.chat.id, f"Вывожу строку {i}")
    elif message.text == "Списание":
        bot.send_message(message.chat.id, "В разработке")
    elif message.text == "Ремонт":
        bot.send_message(message.chat.id, "Скинь фото/фотки и обязательно укажи описание!")
    elif message.text == "Помощь":
        bot.send_message(message.chat.id, "В самом конце тут будут описаны команды, особенности и способ управления ботом")
    elif message.text == "Да":
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Заказ")
        button_comment = types.KeyboardButton("Комментарий")
        button_go = types.KeyboardButton("Отправить на доставку")
        buttons.add(button_drinks, button_comment, button_go)
        order.append(f"{info['drink']}")
        addresses.append(f"{info['address']}")
        quant.append(f"{info['quantity']}")
        bot.send_message(message.chat.id, "Если требуется добавить что-либо чего нет в списке, или оставить комментарий - жми Комментарий", reply_markup=buttons)
    elif message.text == "Комментарий":
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Заказ")
        button_go = types.KeyboardButton("Отправить на доставку")
        buttons.add(button_drinks, button_go)
        bot.send_message(message.chat.id, "Напиши коммент и просто отправь его...",
                         reply_markup=buttons)
    elif message.text == "Отправить на доставку":
        b = ""
        c = 0
        a = 0
        z = ""
        for (i, n, q) in zip(order, addresses, quant):
            a += 1
            b += f"{a}) {i} в количестве: {q} \n"
            db.insert_order(n, i, q)
            db.minus_drink(i, q)
            c += 1
            z = n
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_drinks = types.KeyboardButton("Заказ")
        button_help = types.KeyboardButton("Помощь")
        buttons.add(button_drinks, button_help)
        bot.send_message(message.chat.id, text="Заказ принят, скоро его начнут собирать")
        bot.send_message(admin[0], f"<b>Заказали</b> \n\n{b} на адрес {z} \n\n <b>Комментарий</b> \n\n {comment} ", parse_mode='HTML', reply_markup=buttons)
        order = []
        quant = []
        addresses = []
    """elif message.text:
        comment = message.text
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go = types.KeyboardButton("Отправить на доставку")
        buttons.add(button_go)
        bot.send_message(message.chat.id, "Жмякни на отправку",
                         reply_markup=buttons)"""



@bot.callback_query_handler(func=lambda call:True)
def get_drink(call):
    if call.data == "Пиво":
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_drink(call.data):
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите сорт",  reply_markup=buttons)
        info['type'] = call.data
    elif call.data == "Сидр":
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_drink(call.data):
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите сорт", reply_markup=buttons)
        info['type'] = call.data
    elif call.data == "Лимонады":
        buttons = types.InlineKeyboardMarkup()
        for i in db.get_drink(call.data):
            button = types.InlineKeyboardButton(i, callback_data=i)
            buttons.add(button)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите сорт", reply_markup=buttons)
        info['type'] = call.data
    elif call.data in db.get_drink(info['type']):
        bot.send_message(chat_id=call.message.chat.id, text=f"Введите количество")
        info['drink'] = call.data
        bot.register_next_step_handler(call.message, get_quantity)
    elif call.data in db.get_address():
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_yes = types.KeyboardButton("Да")
        button_no = types.KeyboardButton("Нет")
        buttons.add(button_yes, button_no)
        info['address'] = call.data
        bot.send_message(chat_id=call.message.chat.id, text=f"Заказано {info['drink']} в количестве {info['quantity']}, везем по адресу {info['address']}, правильно?", reply_markup=buttons)


def get_quantity(message):
    info['quantity'] = message.text
    buttons = types.InlineKeyboardMarkup()
    for i in db.get_address():
        button = types.InlineKeyboardButton(i, callback_data=i)
        buttons.add(button)
    bot.send_message(message.chat.id, f"В какой магазин везем?",
                     reply_markup=buttons)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    msg = bot.send_message(message.chat.id, "Оставьте комментарий к фото")
    bot.send_photo(admin[0], message.photo[0].file_id)
    bot.send_message(admin[0], message.caption)
    bot.send_message(message.chat.id, "Добавили поломку в работу")

"""def register_repair(message):
    repair_message = bot.send_message(message.chat.id, "Добавили поломку в работу")
    bot.register_next_step_handler(msg, start_message)"""


bot.infinity_polling(none_stop=True)

'''if __name__ == '__main__':
    print_hi('PyCharm') '''

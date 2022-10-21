import telebot
from telebot import types


bot = telebot.TeleBot("5629208779:AAGwBpAN5L0jjAxpLNAUEaDJZSOJIch96Dk")


@bot.message_handler(commands=['start'])
def send_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = types.KeyboardButton('Вебсайт')
    item2 = types.KeyboardButton('Поддержка')
    item3 = types.KeyboardButton('Комплемент')
    item4 = types.KeyboardButton('Премиум')
    markup.add(item1, item2, item3, item4)

    privet = 'Вас приветствует AJAJAJAJA_Company\nВыберите команду: '
    bot.send_message(message.chat.id, privet, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Вебсайт':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Ajajajaja.com', url='https://www.youtube.com/watch?v=rdi7G1hY4-w'))
            bot.send_message(message.chat.id, 'Приятного просмотра🍿:', reply_markup=markup)
        elif message.text == 'Поддержка':
            bot.send_message(message.chat.id, 'Можете обратиться к нашему партнёру @Personwithoutnameforlife')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton('Оставить контакт', request_contact=True)
            back = types.KeyboardButton('Назад')
            markup.add(item1, back)
            bot.send_message(message.chat.id, 'Или можете оставить контакт,мы с вами свяжемся', reply_markup=markup)
        elif message.text == 'Комплемент':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton('Котик ♥️')
            back = types.KeyboardButton('Назад')
            markup.add(item1, back)
            bot.send_message(message.chat.id, 'Ты словно кофе для программиста <3', reply_markup=markup)

        elif message.text == 'Премиум':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item = types.KeyboardButton('Почкой??')
            back = types.KeyboardButton('Назад')
            markup.add(item, back)
            kard = 'https://yoomoney.ru/transfer'
            bot.send_message(message.chat.id, f"Или картой{kard}", reply_markup=markup)

        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Вебсайт')
            item2 = types.KeyboardButton('Поддержка')
            item3 = types.KeyboardButton('Комплемент')
            item4 = types.KeyboardButton('Премиум')
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, 'Чуть-чуть назад', reply_markup=markup)


bot.polling(none_stop=True)
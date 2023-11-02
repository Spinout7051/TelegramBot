from telebot import types

from loader import bot


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/lowprice')
    btn2 = types.KeyboardButton('/highprice')
    btn3 = types.KeyboardButton('/bestdeal')
    btn4 = types.KeyboardButton('/history')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text='Выберите интересующий пункт меню:', reply_markup=markup)

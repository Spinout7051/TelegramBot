from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.getdata import get_hotel_data, get_journal_data, get_user_data
from loader import bot


BNT_PREFIX = 'bnt_id_'


@bot.message_handler(commands=['history'])
def history(message):
    bot.send_message(message.chat.id, text='Ваши последние запросы:')
    db_data = get_user_data(message.from_user.id)
    for row in db_data:
        date = row.date.strftime('%Y-%m-%d %H:%M:%S')
        text_message = (
            f'{row.command_name.upper()}\n'
            f'Дата: {date}\n'
            f'Город поиска: {row.search_city}\n'
            f'Количество отелей: {row.hotels_count}\n'
        )
        if row.command_name == 'bestdeal':
            text_message = text_message + f'Диапазон цен: {row.price_range}\n' \
                                          f'Диапазон расстояния до центра: {row.town_distance}'

        inline_btn_1 = InlineKeyboardButton('Посмотреть результаты', callback_data=f'{BNT_PREFIX}{row.id}')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
        bot.send_message(message.chat.id, text=text_message, parse_mode='markdown', reply_markup=inline_kb1)


@bot.callback_query_handler(lambda call: call.data.startswith(BNT_PREFIX))
def process_callback_y_button(call):
    db_hotels_data = get_hotel_data(call.data[len(BNT_PREFIX):])
    db_journal_data = get_journal_data(call.data[len(BNT_PREFIX):])
    message = f'Сортировка: {db_journal_data.command_name.upper()}\n' \
              f'Город поиска: {db_journal_data.search_city}\n\n'\

    for data in db_hotels_data:
        text_messg = (
            f'Отель: {data.name}\n'
            f'Адрес: _{data.address}_\n'
            f'Цена: {data.price}\n'
            f'Оценка: {data.overall_score}\n'
            f'Расстояние до центра: {data.distance}\n\n'
        )
        message = message + text_messg

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=message, parse_mode='markdown', reply_markup=None)

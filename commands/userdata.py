from dataclasses import dataclass
from loguru import logger
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import api.api as api
from loader import bot
from commands import bestdeal, highprice, lowprice
from commands.menu import menu


@dataclass
class UserData:
    id_telegram_user: str = ''
    command_name: str = ''
    search_city: str = ''
    hotels_count: int = ''
    need_photos: bool = ''
    photos_count: int = ''
    price_range: list = ''
    town_distance: list = ''


input_user_data = UserData()


@logger.catch
def get_city(message, command_name):
    logger.info(f'{message.from_user.id} set name of city: {message.text}')
    logger.info(f'Checking the entered city name')

    input_user_data.command_name = command_name
    locations_data = api.locations_search(message.text)
    if isinstance(locations_data, dict):
        for sr in locations_data.get('sr'):
            if sr.get('type') == 'CITY':
                input_user_data.search_city = sr.get('regionNames').get('fullName')
                input_user_data.id_telegram_user = message.from_user.id
                bot.send_message(message.from_user.id, 'Сколько отелей найти? (не больше 25):')
                bot.register_next_step_handler(message, get_hostel_count)
                break
        else:
            bot.send_message(message.from_user.id, 'К сожалению, произошла ошибка. Пожалуйста, попробуйте позже.')
            logger.info(f'error checking the entered city name')
            menu(message)
            return


@logger.catch
def get_hostel_count(message):
    if not message.text.isnumeric() or int(message.text) >= 26:
        logger.info(f'{message.chat.id} set number of hotels: {message.text}, the number of is incorrect')
        bot.send_message(message.chat.id, text='Количество некорректно!')
        menu(message)
        return
    logger.info(f'{message.chat.id} set number of hotels: {message.text}')
    input_user_data.hotels_count = int(message.text)
    need_photos(message)


@logger.catch
def need_photos(message):
    inline_btn_1 = InlineKeyboardButton('Да', callback_data='yes_need_photos')
    inline_btn_2 = InlineKeyboardButton('Нет', callback_data='no_need_photos')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
    bot.send_message(message.chat.id, text='Хотите посмотреть фотографии отелей?', reply_markup=inline_kb1)


@bot.callback_query_handler(lambda call: call.data == 'yes_need_photos')
def process_callback_y_button(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Сколько фотографий каждого отеля показать? (не больше 10)', reply_markup=None)

    input_user_data.need_photos = True
    logger.info(f'{call.message.chat.id} want to get photos of the hotel')
    bot.register_next_step_handler(call.message, get_photos_count)


@bot.callback_query_handler(lambda call: call.data == 'no_need_photos')
def process_callback_n_button(call):
    bot.answer_callback_query(call.id)
    if input_user_data.command_name == 'bestdeal':
        logger.info(f'{call.message.chat.id} does not want to get photos of the hotel')
        input_user_data.need_photos = False
        input_user_data.photos_count = 0
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Пожалуйста, укажите диапазон желаемой стоимости за сутки в долларах, '
                                   'через пробел (например: 100 200). Минимальная стоимость — 1 доллар, '
                                   'максимальная — 3000 долларов.', reply_markup=None)
        bot.register_next_step_handler(call.message, get_price_range)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Подбираем отели по вашим параметрам...', reply_markup=None)
        logger.info(f'{call.message.chat.id} does not want to get photos of the hotel')
        logger.info(f'searching hotels...')
        input_user_data.need_photos = False
        input_user_data.photos_count = 0
        callback = highprice.highprice
        if input_user_data.command_name == 'lowprice':
            callback = lowprice.lowprice

        callback(call.message)


@logger.catch
def get_photos_count(message):
    if not message.text.isnumeric() or int(message.text) >= 10:
        logger.info(f'{message.chat.id} set number of photos: {message.text}, the number of is incorrect')
        bot.send_message(message.chat.id, text='Количество некорректно!')
        menu(message)
        return

    logger.info(f'{message.chat.id} set number of photos: {message.text}')
    input_user_data.photos_count = int(message.text)
    if input_user_data.command_name == 'lowprice':
        bot.send_message(message.chat.id, text='Подбираем отели по вашим параметрам...')
        logger.info(f'searching hotels...')
        lowprice.lowprice(message)
    elif input_user_data.command_name == 'highprice':
        bot.send_message(message.chat.id, text='Подбираем отели по вашим параметрам...')
        logger.info(f'searching hotels...')
        highprice.highprice(message)
    elif input_user_data.command_name == 'bestdeal':
        bot.send_message(message.from_user.id, 'Пожалуйста, укажите диапазон желаемой стоимости за сутки в долларах, '
                                               'через пробел (например: 100 200). Минимальная стоимость — 1 доллар, '
                                               'максимальная — 3000 долларов.')
        bot.register_next_step_handler(message, get_price_range)


@logger.catch
def check_range(range_str):
    logger.info(f'Checking range...')
    price_range_list = range_str.split()

    if len(price_range_list) > 2:
        return False

    for price in price_range_list:
        if not price.isnumeric():
            return False

    price_range_list_int = list(map(int, price_range_list))
    sorted_range_list = sorted(price_range_list_int)
    return sorted_range_list


@logger.catch
def get_price_range(message):
    price_range = check_range(message.text)
    if not price_range:
        logger.info(f'{message.chat.id} set range of price: {price_range}, the range of price is incorrect')
        bot.send_message(message.chat.id, text='Диапазон некорректен!')
        menu(message)
        return

    logger.info(f'{message.chat.id} set range of price: {price_range}')
    input_user_data.price_range = price_range
    bot.send_message(message.from_user.id, 'Пожалуйста, укажите диапазон допустимого расстояния от центра города до '
                                           'отеля в км, через пробел (например: 1 3).')
    bot.register_next_step_handler(message, get_town_distance)


@logger.catch
def get_town_distance(message):
    distance_range = check_range(message.text)
    if not distance_range:
        logger.info(f'{message.chat.id} set range of distance: {message.text}, the range of price is incorrect')
        bot.send_message(message.chat.id, text='Диапазон некорректен!')
        menu(message)
        return

    input_user_data.town_distance = distance_range
    logger.info(f'{message.chat.id} set range of distance: {distance_range}')
    logger.info(f'searching hotels...')
    bot.send_message(message.chat.id, text='Подбираем отели по вашим параметрам...')
    callback = bestdeal.bestdeal
    callback(message)

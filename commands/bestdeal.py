from loguru import logger

from api.hotels import get_hotels
from commands import infooutput, userdata
from commands.menu import menu
from database import savedata
from loader import bot


@bot.message_handler(commands=['bestdeal'])
def start_bestdeal(message):
    text_message = 'Введите город, где нужно найти отель'
    bot.send_message(message.from_user.id, text=text_message)
    bot.register_next_step_handler(message, lambda msg: userdata.get_city(msg, command_name='bestdeal'))


@logger.catch
def bestdeal(message):
    try:
        hotels_data_list = get_hotels(
            city=userdata.input_user_data.search_city,
            hotels_count=userdata.input_user_data.hotels_count,
            need_photos=userdata.input_user_data.need_photos,
            photos_count=userdata.input_user_data.photos_count,
            price_range=userdata.input_user_data.price_range,
            town_distance=userdata.input_user_data.town_distance,
            command_name='bestdeal',
        )
    except AttributeError as exp:
        logger.exception(f'Error! {exp}')
        text_message = 'К сожалению, произошла ошибка. Пожалуйста, попробуйте позже.'
        bot.send_message(message.chat.id, text=text_message, parse_mode='markdown')
        menu(message)
        return

    if hotels_data_list:
        savedata.add_journal_data(search_result_data=hotels_data_list)
        infooutput.information_output(hotels_data_list=hotels_data_list, message=message)
    else:
        text_message = 'К сожалению, по вашему запросу ничего не найдено. ' \
                       'Пожалуйста, попробуйте изменить параметры поиска.'
        bot.send_message(message.chat.id, text=text_message)
        menu(message)

from loguru import logger

from api.hotels import get_hotels
from commands import infooutput, userdata
from commands.menu import menu
from database import savedata
from loader import bot


@bot.message_handler(commands=['highprice'])
def start_high_price(message):
    text_message = 'Введите город в котором нужно найти отель:'
    bot.send_message(message.from_user.id, text=text_message)
    bot.register_next_step_handler(message, lambda msg: userdata.get_city(msg, command_name='highprice'))


@logger.catch
def highprice(message):
    try:
        hotels_data_list = get_hotels(
            city=userdata.input_user_data.search_city,
            hotels_count=userdata.input_user_data.hotels_count,
            need_photos=userdata.input_user_data.need_photos,
            photos_count=userdata.input_user_data.photos_count,
            command_name='highprice',
        )
    except AttributeError as exp:
        logger.exception(f'Error! {exp}')
        text_message = 'Что-то пошло не так, попробуйте позже...'
        bot.send_message(message.chat.id, text=text_message, parse_mode='markdown')
        menu(message)
        return

    savedata.add_journal_data(search_result_data=hotels_data_list)
    infooutput.information_output(hotels_data_list=hotels_data_list, message=message)

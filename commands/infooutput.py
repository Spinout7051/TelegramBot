from loguru import logger
from telebot.types import InputMediaPhoto

from commands import userdata
from loader import bot


@logger.catch
def information_output(hotels_data_list, message):
    for hotel in hotels_data_list:
        # Формируем галерею фотографий отеля если нужно
        if userdata.input_user_data.need_photos:
            media_group = []
            if hotel.get('photos'):
                for url in hotel.get('photos'):
                    media_group.append(InputMediaPhoto(media=url))
                bot.send_media_group(message.chat.id, media=media_group)

        # Формируем текстовое описание отеля
        text_message = (
            f'Город: {userdata.input_user_data.search_city}\n'
            f'Отель: {hotel.get("hotel_name")}\n'
            f'Адрес: _{hotel.get("hotel_address")}_\n'
            f'Цена: {hotel.get("price")}\n'
            f'Оценка: {hotel.get("overallScore")}\n'
            f'Расстояние до центра: {hotel.get("distance")}'
        )

        bot.send_message(message.chat.id, text=text_message, parse_mode='markdown')
